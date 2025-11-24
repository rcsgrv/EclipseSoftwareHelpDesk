# Tests that admin users can view the users page
def test_admin_can_view_users_page(logged_in_admin):
    response = logged_in_admin.get("/users", follow_redirects=True)

    assert response.status_code == 200
    assert b"Users" in response.data 

# Tests that admin users can update user roles
def test_admin_can_update_user_roles(logged_in_admin, non_admin_user):
    response = logged_in_admin.post("/update_admin",
        data={f"user_ids": [str(non_admin_user.id)], f"is_admin_{non_admin_user.id}": "on"},
        follow_redirects=True)
    
    assert response.status_code == 200
    assert b"promoted to administrators" in response.data

# Tests that admin users can delete users
def test_admin_can_delete_user(logged_in_admin, non_admin_user):
    response = logged_in_admin.post(f"/delete_user/{non_admin_user.id}", follow_redirects=True)

    assert response.status_code == 200
    assert b"has been deleted" in response.data 

# Tests that non-admin users cannot view the users page
def test_non_admin_cannot_view_users_page(logged_in_non_admin):
    response = logged_in_non_admin.get("/users", follow_redirects=True)

    assert b'You do not have permission to view this page.' in response.data   

# Tests that non-admin users cannot update user roles
def test_non_admin_cannot_edit_user(logged_in_non_admin, admin_user):
    response = logged_in_non_admin.post("/update_admin",
        data={f"user_ids": [str(admin_user.id)], f"is_admin_{admin_user.id}": "on"},
        follow_redirects=True)
    
    assert b'You do not have permission to update user roles.' in response.data

# Tests that non-admin users cannot delete users
def test_non_admin_cannot_delete_user(logged_in_non_admin, admin_user):
    response = logged_in_non_admin.post(f"/delete_user/{admin_user.id}",
        follow_redirects=True)
    
    assert b'You do not have permission to delete users.' in response.data    