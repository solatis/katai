# Names

Read this before you name a type, a trait, a function, a field, a module or a
file, in code or in a plan.

A name says what sets its thing apart from the things beside it: what it
holds, how its contents are arranged, or what it does. A word that fits any
collection or any piece of code, such as `Values`, `Items`, `Elements`,
`Data`, `Info`, `Manager` or `handle`, is never a name on its own. These
pairs show the difference:

| Fits anything                               | Says what sets it apart |
| ------------------------------------------- | ----------------------- |
| `Data`, for jobs that wait for a worker     | `PendingJobs`           |
| `Items`, for the lines of an invoice        | `InvoiceLines`          |
| `Values`, for samples taken at a fixed rate | `FixedRateSamples`      |
| `Info`, for the display settings of a user  | `DisplayPreferences`    |
| `Manager`, for what retries failed uploads  | `UploadRetrier`         |
| `handle()`, for what records a paid invoice | `record_payment()`      |

A concept has one name in a repository. Where the tree calls a thing
`account`, a change does not call it `user` or `customer`, in a type, a
field, a parameter or a comment. Two names tell the reader that there are
two things.

The verb of a function's name says what the function does. A function
named `get`, `is`, `find` or `validate` changes nothing and reports. A
function that changes state, or that returns a new value built from its
input, is named for that, as `parse_port` and not `validate_port` for a
function that returns the port.

A local name may be one letter where the function's name gives its role:
in `store_user(u)` the reader reads "the user". Two parameters of the same
type whose roles the function's name does not tell apart are spelled out,
as `transfer(source, target, amount)` and not `transfer(a, b, x)`.
