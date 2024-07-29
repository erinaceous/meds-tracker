Authentication / authorization using altcha
===========================================


# The flow

* User requests a new challenge via `/altcha/challenge`.
  * The challenge's expiration in seconds is calculated such that it lasts
    until the start of the following day
* That challenge is stored in a `challenges` table on the persistent DB
  * At midnight daily a worker will clean up expired challenges
* The user solves the challenge and must validate it using `/altcha/validate`.
* The challenge is marked `valid` in the `challenges` table.
* The challenge's signature is then used as an API token in requests to the
  `/reports` API.