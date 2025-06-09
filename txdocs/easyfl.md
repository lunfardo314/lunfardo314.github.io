# EasyFL: a simple functional language

## Introduction

**EasyFL** stands for **E**asy **F**unctional **L**anguage. It is a very simple, LISP-like functional programming language without recursion or an eval function. It is extendable and based on platform-independent bytecode.

> Note: EasyFL is neither a rich programming environment nor a universal programming language, nor even a smart contract language. It is a low-level tool intended for scripting validity constraints of UTXO transactions at the lowest byte level. You may think of it as the assembly language for Proxima UTXO transactions. EasyFL is equivalent to stack-based VMs used in Bitcoin and elsewhere; however, it offers pure functional syntax and semantics, which we find more convenient and verifiable.

The EasyFL compiler, core library, and runtime engine are available at the [EasyFL repository](https://github.com/lunfardo314/easyfl). EasyFL is the scripting language used in Proxima UTXO transactions.

The requirements for such a language and engine are:

* Minimalism and maximum simplicity of the language and runtime semantics
* Easy formal verifiability and potential for efficient zk-proof generation
* Extremely compact bytecode
* Determinism of compilation and interpretation
* Human-readable source code
* Minimal set of hardcoded primitives (_op-codes_)
* Extensibility with higher-level concepts through the language itself 
* Standard library of concepts
* Bounded computational model with no need for gas budgeting, non-Turing complete and verification-oriented. This relates closely to simplicity and the above requirements.

Models like _Bitcoin Script_ and _Algorand VM_ meet most requirements except perhaps verifiability, understandability, and minimalism. To improve understandability, verifiability, and minimalism, we chose a purely functional style over stack-base VM.

Example: The following EasyFL expression, interpreted in the context of a transaction, states that the length of the unlock block for the consumed output must be exactly 96 bytes long:

```go
equal(len(selfUnlockBlock), u64/96)
```

Here we assume:
* The expression is evaluated for a particular consumed UTXO
* The function selfUnlockBlock returns the bytes of the unlock block corresponding to the consumed UTXO. If it does not exist, evaluation panics.

## The language

### Data types

The only data type in EasyFL is the byte array (also called byte slice). It can be empty (zero length).

All EasyFL statements have the form and semantics of a function call that takes byte arrays as arguments and returns a byte array as the result.

Where appropriate, the empty byte array is interpreted as `false`; any non-empty value is interpreted as `true`.

### Expressions
_EasyFL_ source code is any ASCII text with line delimiters.

Any text on a line after `//` is a comment and has no effect on execution.

An expression is text where all whitespace characters (`\n`, `\r`, `\t`, ) are ignored. The source code of an _expression_ is parsed into a sequence of _lexems_. A _lexem_ is an ASCII string separated by delimiters.

The delimiters are: `(`, `)`, and `,`.

The grammar for an expression is:

```
<expression> ::= <funcName>[(<call args>)] || <literal>
```

Meta-symbols `[]` denote optional parts. `<call args>` is a comma-delimited list of `<expression>` elements, which may be omitted.

`<funcName>` refers to a function name either from the library or defined as a literal.
Literals are distinguishable from function names by their syntax (described below).

Each function in the library specifies its `arity` — the number of parameters it takes, ranging from 0 to 7. Embedded library functions may also accept a variable number of arguments within that range.

If a function `fun` takes 0 arguments, the expressions `fun` and `fun()` are equivalent. For example, `selfUnlockParameters` is equivalent to `selfUnlockParameters()` and evaluates to a byte array.

### Literals
_Zero-prefix-trimmed_ integers are big-endian byte representations of integers with all leading zero bytes removed. For example:
* integer `1025` $\rightarrow$ `0x0201`
* $2^{16}+3$ $\rightarrow$ `0x010003`. 
* `0` $\rightarrow$ empty byte array.

Literals are constants, meaning they always evaluate to the same value. Supported literal types include:
* Decimal numbers from `0` to `255`: Represented as a single byte. E.g., `0`, `42`. Values like `1337` are invalid.
* Hexadecimal literals with prefix 0x: Represent byte arrays up to `127` bytes. E.g., `0xff0102` (3 bytes); `0x123` is invalid.
* Prefixed integers:
   * `u16/` → 2-byte big-endian
   * `u32/` → 4-byte big-endian
   * `u64/` → 8-byte big-endian
   * `z16/`, `z32/`, `z64/` → zero-trimmed versions of the above

* Panic literals: `!!!message_text` $\rightarrow$ calls embedded fail function with the message (underscores replaced by spaces).
* Bytecode literals: `x/<hex>` $\rightarrow$ inline EasyFL formulas in bytecode form.
* Function code literals: `#function_name` $\rightarrow$ returns byte-encoded representation of the function code, the _call prefix_.

### Examples of closed expressions
We will later introduce open expressions with parameters, but for now, here are examples of closed expressions—those that evaluate to a fixed value: 

The standard library includes embedded functions such as  `fail`, `concat`, `slice`, `byte`, `tail`, `equal`, `if`, `and`, `or`, `not`, `len8`. 

Some valid expressions:

* `0x` and `z32/0` $\rightarrow$ empty slice
* `slice(0x01020304,1,2)` $\rightarrow$ `0x0203`.
* `slice(0x0102,1,1)` and `byte(0x0102, 1)` $\rightarrow$ `0x02`.
* `concat(1, 5)` → `0x0105`, equivalent to `u16/261`, `z64/261`
* `concat` and `concat()` $\rightarrow$ empty slice (equivalent to `false`, `0x`).
* `equal(concat(1, 5), 0x01ff)` $\rightarrow$ empty slice (`false`)
* `if(0, u16/31415, u32/271828)` $\rightarrow$ `u16/31415`
* `or` and `or()` $\rightarrow$ empty slice (`false`)
* `and` and `and()` $\rightarrow$ `true` (value undefined)

>>>>>  TODO here

### Parameters of the expression
An `expression` can use special function calls `$0`, `$1` ... `$7`.  They represent *open parameters of the expression*. Parameters of the expression will be instantiated with values whenever `expression` is evaluated, i.e. whenever it calls the corresponding `$i` function. The use of the parameter `$i` in the expression means that at least `i+1` arguments must be supplied when `expression` is evaluated.

For example expression `concat($0,$1)` will evaluate to the concatenation of the arguments, provided by the call context and `concat(byte($0,1), byte($0,0), tail($0,2)))` will return byte array with swapped first two bytes. 

Expression parameters can be used at any level of the expression, i.e. `not(not(not(not($0))))` is a correct expression, it will require 1 argument.

Expression `or($3)` will return 4th argument, however all 4 must be supplied in the call context, only first 3 won't be used.

## Library of definition. Compilation. Execution
EasyFL library defines a correspondence between function names, function codes (opcodes) and function descriptors.
Function codes are 1-2 byte long values. 

Library is needed for the compilation from the source to the bytecode and back, as well for the compilation of the bytecode to the executable form. The library provides ledger definitions, shared and trusted between Proxima nodes. It defines determinism of the ledger. If two participants of the distributed system would assume different ledger definitions, they cannot come to the consensus, because what seems to be valid for one, will look invalid to another. 

### Function definitions
Expression, which may or may not have open parameters, can be assigned the name and thus become part of the library, used to validate transactions.

The syntax we use for extending library with the enw function is:
```
func <function name> : <expression>
```
For example
```
func lessOrEqualTo : or(lessThan($0, $1), equalUint($0,$1))
```
defines a function with two arguments for the relation $\le$ between byte arrays, interpreted as big-endian integers.

In the library, definition of the function takes form of a _function descriptor_.

### Bytecode
So far we introduced the _source form_ of the expression. The source is a human-readable form, while the canonical form of expression, used in libraries and embedded in the transactions, is its **bytecode**.

The _bytecode_ of the expression is a compressed form of it with names of functions encoded. 
The bytecode is **compiled** from the source, using the library of functions (see below [library](#library-of-functions)), which assigns codes to the function names. 

Note, that the bytecode may equally represent a closed formula (used in transactions), or open formula with parameters (used in the library)

The $code(\cdot)$ function denotes compilation: $code(source) \rightarrow bytecode$. In _EasyFL_ compilation is essentially a serialization of the source code to the bytecode.

Let's say we have source expression $E = fn(e_0, \dots e_{n-1})$, where $fn$ is function name and $e_i$ is expression source. Then serialized form of the expression, the bytecode is the following concatenation:  
$$
code(E) = callPrefix(fn)||code(e_0)||\dots ||code(e_{n-1})
$$

We will not define exact format of the $callPrefix(f)$ (it can be found in the open repository), just will say here it is 1 to 3 bytes which point to the particular function in the library and, specifies number of call arguments, the call _arity_. 

The source expression is recursively compiled to the nested array of bytecodes, down to the terminal elements. The terminal elements are function calls without parameters:
* calls to parameter-less library functions
* the literals (see [above](#literals)), which usually define inline data such as `123`, `u32/1337` or `0x01ff` 
* the parameter calls `$0`, `$1`.., which are special function, which evaluates argument expressions

### Library of functions

[Here](txdocs/library_base.md) we provide base EasyFL library in the form of the _YAML_ file. In the Proxima ledger, the base library is extended with additional functions, specific to the Proxima transactions.  

The library is a list of function descriptors. Function descriptor take a form: 
```
      sym: <function name>
      description: <free description of the purpose>
      funCode: <function code>
      numArgs: <number of parameters. -1 mean vararg>
      embedded: <true for embeded (hardcoded) functions, false for EasyFL expressions>
      short: <true for short code (up to 63), long  >
      bytecode: <if embedded=false, hex-encoded bytecode of the expression>
      source: <if embedded=false, source of the expression>
```
For the ledger definitions, the library is immutable:

- it must be sorted in the ascending order of function codes
- it has `hash: ..` keyword, which is `blake2b-256` hash of concatenated following data elements: 
  - function names
  - function codes
  - number of arguments
  - embedded flag
  - the bytecode (if relevant)
- for formula elements (with embedded=false), compiled source code must be equal to the bytecode

When library is loaded into the environment which interprets it (node, wallet and similar), consistency of the library definitions is checked. Library contains all the information needed to check for its consistency. 

The embedded functions are implemented outside the library, by the node. They must be provided upon instantiating library and starting reading tge ledger state and transactions.

The genesis ledger genesis is created with the particular library definitions, called `ledger ID`. After the genesis ledger state is created, library of definitions becomes an immutable part of the ledger state. 

### Extending the library
Normally we treat the library of definition as an atomic, immutable object.
However, before the ledger starts its existence, the base library is extended with new functions. For example, Proxima extends base library, provided by the EasyFL with functions needed for the Proxima transaction model. The resulting library becomes immutable part of the Proxima ledger. 

Let's say we have library $L$ and want to extend it with the new function. This will result in new library $L'$. Requirements for such operation:
- **no recursion**: if we are adding a new EasyFL formula with the new function name to the existing library, the expression can only use function names already present in the library
- **backward compatibility of bytecodes**: function code (opcode) of the new function must be strictly larger that all the opcodes in its category (short embedded, long embedded and extended has different ranges of their opcodes). This will ensure, that any bytecode used in transaction created for the library $L$ will be valid with the library $L'$.

This way, after we modify the library with several new functions, embedded and expressions, the old library $L$ will remain compatible with the new library $L'$ in a sense, that old valid transaction will remain valid with the upgraded library. 

The hash of the upgraded library will change. Taking into account all of this, **we can ensure upgrades in the ledger (hard forks) without losing backward compatibility**. 

### Evaluation of expressions
Expressions are evaluated in the form of the internal evaluation tree, derived from the bytecode. So, the workflow is always like this:

`<expression source> -> <bytecode> -> <evaluation tree> -> <evaluation>`.

Each script/formula is evaluated in the context of the transaction, i.e. script expression should be able to access the (immutable) context. For this reason, EasyFL engine ensures means of providing evaluation context to the expression interpreted. The script of the expression accesses parts of the evaluation context (the transaction) via special embedded functions.

Evaluation steps:
- convert bytecode to a tree-like evaluation form
- provide evaluation context, usually the _transaction context_.
- run evaluation recursively along the tree down to the terminal data elements (embedded functions)

The evaluation engine (function `EvalExpression` in Go implementation) is using **lazy evaluation**. It means argument expression is only evaluated when and if it is needed for the evaluation of the context where it is used as a parameter. For example, the expression:
`if(concat, byte(0,1), 0x01)` will never panic even if `byte(0,1)` always panics (see [Exceptions](#exceptions) below). It is because `concat` always returns `false` and `if` function always evaluates only one of two branches.

### Exceptions
Evaluation of the expression may fail with the panic. For example, expression `byte(0,1)` will always panic, because it tries to take a byte with index `1` from the 1-byte array `[0]`.

The embedded function `fail` always panics with its only argument interpreted as the error message/string. The `!!!<msg>` is a shortcut literal of the `fail` function call.

The evaluation engine (the Go function `EvalFromBinary` in Go implementation) does not process exceptions. The transaction validation context, which invokes the evaluation engine, must intercept panic and treat transaction as invalid.

### Examples
* `if($0,$2,$1)` will evaluate `$2` if `$0` will return true and will evaluate `$1` if `$0` is nil. It deserves the name `ifNot`.
* `concat($0, $0, $0, $0)` will repeat argument by concatenating it 4 times.

In Go, the expressions can be evaluated the following way:

```go
ret, err := easyfl.EvalFromSource(nil, "concat($1,$0)", []byte{222}, []byte{111})
```
will compile the source to the bytecode form, will evaluate it with provided arguments and will return reversed slice:
```go
[]byte{111,222}
```
