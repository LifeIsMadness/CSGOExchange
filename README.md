# Steam OpenId authentication with python-social-auth

This application shows how to create a django app with steam openid
authentication using the steam backend in the package python-social-auth.

**This repository aims to authenticate users ONLY via steam.**

The contains the necessary configuration for the backend and uses a
custom user model in order to process all the
[extra data](https://developer.valvesoftware.com/wiki/Steam_Web_API#GetPlayerSummaries_.28v0002.29)
retrieved from the Web-API.
