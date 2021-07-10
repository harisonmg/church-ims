# URLconf

| URL | View | Who can access |
| --- | ---- | -------------- |
| `/` | `core:index` | everyone |
| `/accounts/register/` | `accounts:register` | everyone |
| `/accounts/login/` | `accounts:login` | everyone |
| `/accounts/password_change/` | `accounts:password_change` | everyone |
| `/accounts/password_change/done/` | `accounts:password_change_done` | everyone |
| `/accounts/password_reset/` | `accounts:password_reset` | everyone |
| `/accounts/password_reset/done/` | `accounts:password_reset_done` | everyone |
| `/accounts/reset/<uidb64>/<token>/` | `accounts:password_reset_confirm` | everyone |
| `/accounts/reset/done/` | `accounts:password_reset_complete` | everyone |
| `/accounts/settings/` | `accounts:settings_detail` | current logged-in user |
| `/accounts/settings/update/` | `accounts:settings_update` | current logged-in user |
| `/accounts/<username>/` | `accounts:profile_detail` | current logged-in user |
| `/accounts/<username>/update/` | `accounts:profile_self_update` | current logged-in user |
| `/dashboard/` | `core:dashboard` | current logged-in user |
| `/people/` | `people:person_list` | staff |
| `/people/add_child/` | `people:child_create` | any logged-in user |
| `/people/<username>/` | `people:person_detail` | person creator, staff |
| `/people/<username>/update/` | `people:person_update` | person creator, staff |
| `/people/<username>/relatives/` | `people:relationships_by_user_list` | current logged-in user, staff |
| `/people/relationships/` | `people:relationship_list` | staff |
| `/people/relationships/add/` | `people:relationship_create` | any logged-in user |
| `/people/relationships/<uuid>/` | `people:relationship_detail` | relationship creator |
| `/people/relationships/<uuid>/update/` | `people:relationship_update` | relationship creator, staff |
| `/people/relationships/<uuid>/delete/` | `people:relationship_delete` | relationship creator, staff |
| `/records/temperature/` | `records:list` | staff |
| `/records/temperature/<username>/` | `records:list_by_user` | current logged-in user, staff |
| `/records/temperature/<username>/add/` | `records:add` | staff |

## Notes
- _current logged-in user_ means the information displayed is specific to that user
- _person creator_ means the user who added a relative
