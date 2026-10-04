import streamlit as st 
import requests
import os
 



# Fallback to your live FastAPI Render URL
BASE_URL=os.environ.get("BaCKEND_URL",'https://todo-app-e1ar.onrender.com/') 

st.title("My FastAPI + Streamlit App")

if st.button("Fetch Data from Backend"):
    # Call your live FastAPI endpoint
    response = requests.get(f"{BASE_URL}/docs")
    if response.status_code == 200:
        st.write(response.json())
    else:
        st.error("Failed to connect to backend")


# 1. Initialize session storage to persist the JWT token across user actions
if "token" not in st.session_state:
    st.session_state.token = None

# 2. Authentication View (Visible if user hasn't successfully logged in yet)
if st.session_state.token is None:
    # Sidebar navigation options to let users switch tabs
    auth_mode = st.sidebar.selectbox("Choose Action", ["Login", "Register Account"])

    if auth_mode == "Register Account":
        st.subheader("Create a New Account")
        reg_username = st.text_input("Username")
        reg_email = st.text_input("Email")
        reg_first_name = st.text_input("First Name")
        reg_last_name = st.text_input("Last Name")
        reg_phone = st.text_input("Phone Number")
        reg_password = st.text_input("Password", type="password")
        reg_role = st.selectbox("Role", ["user", "admin"])

        if st.button("Submit Registration"):
            # Payload matching CreateUserRequest on the backend
            registration_payload = {
                "username": reg_username,
                "email": reg_email,
                "first_name": reg_first_name,
                "last_name": reg_last_name,
                "password": reg_password,
                "role": reg_role,
                "phone_number": reg_phone
            }
            
            # Submits user schema info as JSON to the router base path
            reg_response = requests.post(f"{BASE_URL}/auth/", json=registration_payload)
            
            if reg_response.status_code == 201:
                st.success("Account created successfully! Now switch to the Login tab.")
            else:
                st.error(f"Registration failed: {reg_response.text}")

    elif auth_mode == "Login":
        st.subheader("Login to Your Account")
        login_username = st.text_input("Username")
        login_password = st.text_input("Password", type="password")
        
        if st.button("Log In"):
            # Form-data dictionary required by your backend's OAuth2PasswordRequestForm
            login_form_data = {
                "username": login_username,
                "password": login_password
            }
            
            # Hits the precise token generation endpoint shown in your image
            login_response = requests.post(f"{BASE_URL}/auth/token", data=login_form_data)
            
            if login_response.status_code == 200:
                # Extracts the 'access_token' value returned on line 113 of your backend code
                st.session_state.token = login_response.json().get("access_token")
                st.success("Login successful! Loading your interface...")
                st.rerun()
            else:
                st.error("Authentication failed. Invalid username or password.")

# 3. Authorized View (Visible only when st.session_state.token holds a valid key)
else:
    # Sidebar logout panel option
    if st.sidebar.button("Log Out"):
        st.session_state.token = None
        st.rerun()

    st.title("Todo-App")
    st.header("create a new todo item")
    
    todo_id = st.number_input('ID', min_value=0, step=1)
    todo_title = st.text_input('Title')
    todo_description = st.text_area('Description')
    todo_priority = st.number_input('Priority', min_value=0, step=1)
    
    # Checkbox passes a pure boolean (True/False) value required by Pydantic
    todo_complete = st.checkbox("Complete") 
    
    if st.button("Add to-do"):
        # Injects the security token directly into the Authorization header to pass user_dependency checks
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        
        todo_payload = {
            "id": todo_id,
            "title": todo_title,
            "description": todo_description,
            "priority": todo_priority,
            "complete": todo_complete
        }
        
        response = requests.post(f"{BASE_URL}/todos/todo", json=todo_payload, headers=headers)
        
        if response.status_code == 201:
            st.success("todo item is added successfully")
        else:
            error_msg = response.json().get('detail', 'Could not save the item.')
            st.error(f"Error: {error_msg}")




 
    # Button to trigger fetching data
    if st.button("Refresh Task List", key="refresh_all_todos"):
        # Passing token data to satisfy the backend 'user: user_dependency' check
        headers = {
            "Authorization": f"Bearer {st.session_state.get('token', '')}"
        }
        
        try:
            # Sends the GET request directly to your exact backend route format: /
            # If your router has a prefix like /todo, adjust this to f"{BASE_URL}/todo/"
            response = requests.get(f"{BASE_URL}/todos/", headers=headers)
            
            # 1. Handling successful response matching HTTP_200_OK
            if response.status_code == 200:
                todos = response.json()
                
                if not todos:
                    st.info("You don't have any tasks saved yet.")
                else:
                    st.success(f"Successfully loaded {len(todos)} tasks!")
                    
                    # Loop through and display each item dynamically
                    for todo in todos:
                        status_emoji = "✅" if todo.get("complete") else "⏳"
                        
                        with st.container():
                            st.markdown(f"### {status_emoji} **{todo.get('title')}** (ID: {todo.get('id')})")
                            st.write(f"**Description:** {todo.get('description')}")
                            st.write(f"**Priority:** Level {todo.get('priority')}")
                            st.divider() # Adds a clean separation line between tasks
                            
            # 2. Matches your backend raise exception: status_code=401, detail='Authentication Failed'
            elif response.status_code == 401:
                st.error("🔒 Authentication Failed! Check your user login session details.")
                
            else:
                st.error(f"⚠️ Unexpected Error {response.status_code}: {response.text}")
                
        except requests.exceptions.ConnectionError:
            st.error("🔌 Connection Refused. Please check if your FastAPI Uvicorn server is actively running.")
        
   
 
    st.sidebar.subheader("🔍 Find Task by ID")

    # Force input as an integer to prevent a 422 error
    search_id = st.sidebar.number_input("Enter Todo ID", min_value=1, step=1, value=1)

    if st.sidebar.button("Search Task"):
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        
        # Clean URL path targeting your exact @router.get("/todo/{todo_id}") setup
        target_url = f"{BASE_URL}/todos/todo/{int(search_id)}"
        
        try:
            search_response = requests.get(target_url, headers=headers)
            
            if search_response.status_code == 200:
                single_todo = search_response.json()
                st.sidebar.success(f"🎉 Found Task #{search_id}!")
                st.sidebar.markdown(f"**Title:** {single_todo.get('title')}")
                st.sidebar.write(f"**Description:** {single_todo.get('description')}")
                
            elif search_response.status_code == 404:
                # Captures your backend's custom detail string ('Todo not found.')
                error_details = search_response.json().get('detail', 'Not Found')
                st.sidebar.warning(f"❌ Backend says: {error_details}")
                st.sidebar.caption("Note: This ID either doesn't exist or belongs to another user account.")
                
            elif search_response.status_code == 401:
                st.sidebar.error("🔒 Authentication Failed! Your token might be expired.")
                
            else:
                st.sidebar.error(f"Error Code: {search_response.status_code}")
                st.sidebar.write(search_response.json())
                
        except requests.exceptions.ConnectionError:
            st.sidebar.error("Could not reach the FastAPI server. Is it running?")





 


    # Form component to handle user input securely
    st.header('update to-do')
    with st.form("update_todo_form"):
        # 1. Path Parameter: todo_id (Validated with Path(gt=0) in your backend)
        todo_id = st.number_input("Todo ID (Must be greater than 0)", min_value=1, step=1, value=1)
        
        st.markdown("---")
        st.subheader("Todo Request Body fields:")
        
        # 2. Request Body: Matches fields being reassigned in your code
        title = st.text_input("New Title")
        description = st.text_area("New Description")
        priority = st.slider("New Priority Level", min_value=1, max_value=5, value=3)
        complete = st.checkbox("Mark Task as Completed")
        
        # Submit button
        submit_button = st.form_submit_button(label="Update Task")

    if submit_button:
        # Constructing payload matching your TodoRequest validation model
        payload = {
            "title": title,
            "description": description,
            "priority": priority,
            "complete": complete
        }
        
        # Passing token/session data to satisfy your backend's 'user_dependency'
        # Adjust authentication header styling depending on how your dependency reads it
        headers = {
            "Authorization": f"Bearer {st.session_state.get('token', '')}"
        }
        
        try:
            # Sends the PUT request directly to your exact backend route format
            response = requests.put(
                f"{BASE_URL}/todos/todo/{todo_id}",
                json=payload,
                headers=headers
            )
            
            # 3. Handling responses matching your specific backend raise conditions:
            if response.status_code == 204:
                st.success(f"✅ Success! Todo #{todo_id} has been modified and saved to the database.")
                
            elif response.status_code == 401:
                # Matches: raise HTTPException(status_code=401, detail='Authentication Failed')
                st.error("🔒 Authentication Failed! Check your user session.")
                
            elif response.status_code == 404:
                # Matches: raise HTTPException(status_code=404, detail='Todo not found.')
                st.error("🔎 Todo Not Found! The ID doesn't exist or it doesn't belong to this user.")
                
            else:
                st.error(f"⚠️ Unexpected Error {response.status_code}: {response.text}")
                
        except requests.exceptions.ConnectionError:
            st.error("🔌 Connection Refused. Please check if your FastAPI Uvicorn server is actively running.")



    st.header("Delete a Todo Item")
    

    # Form to take input safely
    with st.form("delete_todo_form"):
        # Path Parameter: validated with Path(gt=0) in your FastAPI code
        delete_id = st.number_input("Enter Todo ID to Delete", min_value=1, step=1, value=1)
        
        # Submit button for form container
        submit_delete = st.form_submit_button("Delete Task")

    if submit_delete:
        # satisfying your 'user: user_dependency' in the backend
        headers = {
            "Authorization": f"Bearer {st.session_state.get('token', '')}"
        }
        
        try:
            # Constructing the exact path parameter endpoint -> /todo/{todo_id}
            target_url = f"{BASE_URL}/todos/todo/{delete_id}"
            
            # Sending the HTTP DELETE request
            response = requests.delete(target_url, headers=headers)
            
            # Checking status codes based strictly on your backend logic
            if response.status_code == 204:
                # Matches: status_code=status.HTTP_204_NO_CONTENT
                st.success(f"🗑️ Todo #{delete_id} has been successfully deleted from your database!")
                
            elif response.status_code == 401:
                # Matches: raise HTTPException(status_code=401, detail='Authentication Failed')
                st.error("🔒 Authentication Failed: Invalid or expired session.")
                
            elif response.status_code == 404:
                # Matches: raise HTTPException(status_code=404, detail='Todo not found.')
                st.error("🔎 Todo Not Found: The item does not exist or does not belong to you.")
                
            else:
                st.error(f"⚠️ Unexpected Error {response.status_code}: {response.text}")
                
        except requests.exceptions.ConnectionError:
            st.error("🔌 Connection Refused: Ensure your backend FastAPI app is running.")