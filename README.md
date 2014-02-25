toggle
======

Simple couchdb-backed django app for doing user and domain level toggles.

Is designed to be _simple_ and _fast_ (automatically caches all toggles).

To use, make sure `toggle` is in your `INSTALLED_APPS` and `COUCHDB_DATABASES`.

To create a toggle:

```
./manage.py make_toggle mytogglename user1@example.com user2@example.com
./manage.py make_toggle mytogglename -t domain qa-domain test-domain
```

To toggle a feature in code:

```python

# toggle_enabled(<name_of_toggle>, <entity_type>, <entity_string>)
if toggle_enabled('mytogglename', 'user', someuser.username):  # checking users
    do_toggled_work()
else:
    do_normal_work()
```
