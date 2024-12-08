# CHANGELOG.md

## 0.0.6.4rc0

Features:

  - Fix recursion issue happening at token expiration time

## 0.0.6.3

  - Implement refresh token api for panels with version > 4.13.2
  - Improve websocket connection handling
  - Reduce wait time before reconnecting to websocket in case of connection drop
  - Improve tests

## v0.0.6.2

Features:

  - Fix wrong protocol check to better handle https/wss endpoints with SSL
  - Handle pipy dependency to explicitly point to the new asyncio implementation


## v0.0.6.1

Features:

  - Relax websockets dependency to facilitate integration with other platforms

## v0.0.6

Features:

  - Fix websockets dependency issues

## v0.0.5

Features:

  - Added CHANGELOG
  - Releasing stable version

## v0.0.5rc3

Bugfixes:

  - Fix push_feature

## v0.0.5rc2

Features:

  - Expose BASE_URL and SSL_CONTEXT to via properties

## v0.0.4

Features:

  - Handle 422 status code

## v0.0.3rc4

Features:

  - Improve error handling for local API calls


