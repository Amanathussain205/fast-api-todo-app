import streamlit as st
import requests
from urllib.parse import quote


# =========================================================
# CONFIGURATION
# =========================================================

API_URL = "http://127.0.0.1:8000"


# =========================================================
# API FUNCTIONS
# =========================================================

def get_todos():
    """Get all Todos from FastAPI."""

    response = requests.get(
        f"{API_URL}/todos"
    )

    if response.status_code == 200:
        return response.json()

    return []


def create_todo(title, file):
    """Create one Todo with optional file."""

    data = {
        "title": title
    }

    files = None

    if file is not None:

        files = {
            "file": (
                file.name,
                file.getvalue(),
                file.type
            )
        }

    response = requests.post(
        f"{API_URL}/todos",
        data=data,
        files=files
    )

    return response


def update_todo(
    todo_id,
    title,
    completed,
    file=None,
    remove_file=False
):
    """Update Todo title, status and optional file."""

    data = {
        "title": title,
        "completed": str(completed).lower(),
        "remove_file": str(remove_file).lower()
    }

    files = None

    # Add replacement file if provided
    if file is not None:

        files = {
            "file": (
                file.name,
                file.getvalue(),
                file.type
            )
        }

    response = requests.put(
        f"{API_URL}/todos/{todo_id}",
        data=data,
        files=files
    )

    return response


def delete_todo(todo_id):
    """Delete one Todo."""

    response = requests.delete(
        f"{API_URL}/todos/{todo_id}"
    )

    return response


def delete_all_todos():
    """Delete all Todos."""

    response = requests.delete(
        f"{API_URL}/todos"
    )

    return response


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Todo App",
    page_icon="✅",
    layout="centered",
)


# =========================================================
# HEADER
# =========================================================

st.title("✅ Todo App")
st.caption("Stay organized. Get things done.")


# =========================================================
# LOAD TODOS
# =========================================================

todos = get_todos()


# =========================================================
# DASHBOARD
# =========================================================

total_todos = len(todos)

completed_todos = sum(
    todo["completed"]
    for todo in todos
)

pending_todos = total_todos - completed_todos


col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total", total_todos)

with col2:
    st.metric("Completed", completed_todos)

with col3:
    st.metric("Pending", pending_todos)


st.divider()


# =========================================================
# ADD TODO
# =========================================================

st.subheader("➕ Add New Todo")

with st.form("add_todo_form"):

    title = st.text_input(
        "Post",
        placeholder="Write your Todo..."
    )

    uploaded_file = st.file_uploader(
        "Attach an image or file (optional)",
        key="new_todo_file"
    )

    submitted = st.form_submit_button(
        "Add Todo",
        use_container_width=True
    )

    if submitted:

        if not title.strip():

            st.warning("Please enter a Todo.")

        else:

            response = create_todo(
                title,
                uploaded_file
            )

            if response.status_code == 201:

                st.success(
                    "Todo added successfully!"
                )

                st.rerun()

            else:

                st.error(
                    f"Failed to create Todo. "
                    f"Server response: {response.text}"
                )


st.divider()


# =========================================================
# TODO LIST HEADER
# =========================================================

st.subheader("📋 My Todos")


# =========================================================
# FILTER
# =========================================================

filter_option = st.radio(
    "Filter",
    ["All", "Pending", "Completed"],
    horizontal=True
)


if filter_option == "Pending":

    displayed_todos = [
        todo
        for todo in todos
        if not todo["completed"]
    ]

elif filter_option == "Completed":

    displayed_todos = [
        todo
        for todo in todos
        if todo["completed"]
    ]

else:

    displayed_todos = todos


# =========================================================
# DELETE ALL TODOS
# =========================================================

if todos:

    if st.button(
        "🗑️ Delete All Todos",
        use_container_width=True
    ):

        response = delete_all_todos()

        if response.status_code == 200:

            st.success(
                "All Todos deleted successfully!"
            )

            st.rerun()

        else:

            st.error(
                f"Failed to delete all Todos. "
                f"Server response: {response.text}"
            )


st.divider()


# =========================================================
# DISPLAY TODOS
# =========================================================

if not displayed_todos:

    st.info("No Todos found.")

else:

    for todo in displayed_todos:

        todo_id = todo["id"]
        title = todo["title"]
        completed = todo["completed"]
        file_path = todo.get("file_path")

        with st.container(border=True):

            # =================================================
            # TODO INFORMATION
            # =================================================

            if completed:

                st.markdown(
                    f"### ~~{title}~~"
                )

                st.success("✅ Completed")

            else:

                st.markdown(
                    f"### {title}"
                )

                st.warning("⏳ Pending")


            # =================================================
            # ATTACHED FILE
            # =================================================

            if file_path:

                # Get filename from database path
                filename = file_path.split("/")[-1]

                # URL-encode filename
                encoded_filename = quote(
                    filename,
                    safe=""
                )

                # Create proper browser URL
                file_url = (
                    f"{API_URL}/uploads/{encoded_filename}"
                )

                lower_filename = filename.lower()

                if lower_filename.endswith(
                    (".png", ".jpg", ".jpeg", ".gif", ".webp")
                ):

                    st.image(
                        file_url,
                        caption="Attached image"
                    )

                else:

                    st.markdown(
                        f"[📎 Open attached file]({file_url})"
                    )


            # =================================================
            # BUTTONS
            # =================================================

            col1, col2, col3 = st.columns(3)


            # =================================================
            # COMPLETE / UNCOMPLETE
            # =================================================

            with col1:

                if completed:
                    button_text = "↩️ Undo"
                else:
                    button_text = "✅ Complete"

                if st.button(
                    button_text,
                    key=f"complete_{todo_id}",
                    use_container_width=True
                ):

                    response = update_todo(
                        todo_id,
                        title,
                        not completed
                    )

                    if response.status_code == 200:

                        st.rerun()

                    else:

                        st.error(
                            f"Failed to update Todo: "
                            f"{response.text}"
                        )


            # =================================================
            # EDIT
            # =================================================

            with col2:

                if st.button(
                    "✏️ Edit",
                    key=f"edit_{todo_id}",
                    use_container_width=True
                ):

                    st.session_state[
                        f"editing_{todo_id}"
                    ] = True

                    st.rerun()


            # =================================================
            # DELETE
            # =================================================

            with col3:

                if st.button(
                    "🗑️ Delete",
                    key=f"delete_{todo_id}",
                    use_container_width=True
                ):

                    response = delete_todo(
                        todo_id
                    )

                    if response.status_code == 200:

                        st.success(
                            "Todo deleted!"
                        )

                        st.rerun()

                    else:

                        st.error(
                            f"Failed to delete Todo: "
                            f"{response.text}"
                        )


            # =================================================
            # EDIT FORM
            # =================================================

            if st.session_state.get(
                f"editing_{todo_id}",
                False
            ):

                st.markdown("#### ✏️ Edit Todo")

                # ---------------------------------------------
                # TITLE
                # ---------------------------------------------

                new_title = st.text_input(
                    "Todo title",
                    value=title,
                    key=f"title_input_{todo_id}"
                )


                # ---------------------------------------------
                # FILE REPLACEMENT
                # ---------------------------------------------

                new_file = st.file_uploader(
                    "Replace attached file (optional)",
                    key=f"file_input_{todo_id}"
                )


                # ---------------------------------------------
                # REMOVE EXISTING FILE
                # ---------------------------------------------

                remove_file = False

                if file_path:

                    remove_file = st.checkbox(
                        "🗑️ Remove current attached file",
                        key=f"remove_file_{todo_id}"
                    )


                edit_col1, edit_col2 = st.columns(2)


                # =================================================
                # SAVE
                # =================================================

                with edit_col1:

                    if st.button(
                        "💾 Save Changes",
                        key=f"save_{todo_id}",
                        use_container_width=True
                    ):

                        if not new_title.strip():

                            st.warning(
                                "Todo title cannot be empty."
                            )

                        elif new_file is not None and remove_file:

                            st.warning(
                                "Choose either a replacement "
                                "file OR remove the current file."
                            )

                        else:

                            response = update_todo(
                                todo_id,
                                new_title,
                                completed,
                                new_file,
                                remove_file
                            )

                            if response.status_code == 200:

                                st.session_state[
                                    f"editing_{todo_id}"
                                ] = False

                                st.success(
                                    "Todo updated successfully!"
                                )

                                st.rerun()

                            else:

                                st.error(
                                    f"Failed to update Todo: "
                                    f"{response.text}"
                                )


                # =================================================
                # CANCEL
                # =================================================

                with edit_col2:

                    if st.button(
                        "❌ Cancel",
                        key=f"cancel_{todo_id}",
                        use_container_width=True
                    ):

                        st.session_state[
                            f"editing_{todo_id}"
                        ] = False

                        st.rerun()