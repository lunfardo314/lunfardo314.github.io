# EasyFL: a simple functional language

## Introduction

**EasyFL** stands for **E**asy **F**unctional **L**anguage. It is a very simple, functional programming language with LISP-like syntax and without recursion and `eval` function. It is extendable and based on platform-independent bytecode.

> Note: EasyFL is neither a rich programming environment nor a universal programming language, nor even a smart contract language. It is a low-level tool intended for scripting validity constraints of UTXO transactions at the lowest byte level. You may think of it as the assembly language for Proxima UTXO transactions. EasyFL is equivalent to stack-based VMs used in Bitcoin and elsewhere; however, it offers pure functional syntax and semantics, which we find more convenient and verifiable.

The EasyFL compiler, core library, and runtime engine are available at the [EasyFL repository](https://github.com/lunfardo314/easyfl). 

EasyFL is the scripting language used to express trustless, finite, and verifiable constraints in UTXO transactions that produce or spend UTXOs. These constraints form what are often called **covenants**. They enforce certain properties of transactions and, therefore, certain behavior of transaction producers.

Such a language meets the following set of requirements:

* Minimalism and maximum simplicity of the language and runtime semantics
* Platform-independence
* Extremely compact bytecode
* Determinism of compilation and interpretation
* Human-readable source code
* Minimal set of hardcoded primitives (_op-codes_)
* Extensibility with higher-level concepts through the language itself 
* Standard library of concepts
* Bounded computational model with no need for gas budgeting, non-Turing complete and verification-oriented
* Formal verifiability with systems like TLA+
* Easiness for reasoning and validity verification by AI agents
* Low difficulty converting to circuits for zk-based validity proofs

Example: The following EasyFL expression, interpreted in the context of a transaction, states that the length of the unlock block for the consumed output must be exactly 96 bytes long:

```go
equal(len(selfUnlockBlock), u64/96)
```

Here we assume:
* The expression is evaluated for a particular consumed UTXO
* The function `selfUnlockBlock` returns the bytes of the unlock block corresponding to the consumed UTXO. If it does not exist, evaluation panics.

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

`<funcName>` refers to a function name from the library.
Literals are distinguishable from function names by their syntax (described below).

Each function in the library either specifies its `arity` — the number of parameters it takes, ranging from 0 to 15, or is variadic: having variable number of arguments within that range.

If a function `fun` takes 0 arguments, the expressions `fun` and `fun()` are equivalent. For example, `selfUnlockParameters` is equivalent to `selfUnlockParameters()`..

### Literals
By definition, a _zero-prefix-trimmed_ integers are big-endian byte representations of integers with all leading zero bytes removed. Examples:
* integer `1025` $\rightarrow$ `0x0201`
* $2^{16}+3$ $\rightarrow$ `0x010003`. 
* `0` $\rightarrow$ empty byte array.

Literals are constants, meaning they always evaluate to the same value independently on the context. Supported literal types include:
* Decimal numbers from `0` to `255`: Represented as a single byte. E.g., `0`, `42`. Values like `1337` are invalid.
* Hexadecimal literals with prefix `0x`: Represent byte arrays up to $2^16-1$ bytes. E.g., `0xff0102` (3 bytes); `0x123` is invalid. Note that very long data normally are subject to much smaller protocol constraints. 
* Prefixed integers:
   * `u16/` → 2-byte big-endian
   * `u32/` → 4-byte big-endian
   * `u64/` → 8-byte big-endian
   * `z16/`, `z32/`, `z64/` → zero-trimmed versions of the above

* Panic literals: `!!!message_text` $\rightarrow$ calls embedded `fail` function with the message. Underscores are replaced by spaces in the output.
* Bytecode literals: `x/<hex>` $\rightarrow$ inline EasyFL formulas in bytecode form.
* Function code literals: `#function_name` $\rightarrow$ returns byte-encoded representation of the function code, the _call prefix_.

### Examples of closed expressions
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
* `and` and `and()` $\rightarrow$ `true` (specific value undefined)

### Parameters of the expression
Expressions (formulas) can include parameter references:  `$0`, `$1` ... `$14`.  These represent **open parameters** that will be instantiated during evaluation of the formula.
Examples:
* `concat($0,$1)` $\rightarrow$ concatenates two arguments
* `concat(byte($0,1), byte($0,0), tail($0,2)))` $\rightarrow$ swaps first two bytes. 
* `not(not(not(not($0))))` requires one argument.
* `or($3)` returns 4th argument; all 4 must be supplied

For variadic functions the literal `$$` evaluates to the number of actual arguments in the call.

## Library of definition. Compilation. Execution
The EasyFL library maps function names to opcodes and descriptors. Function codes are 1–2 bytes.

The library enables:
* Compilation from source to bytecode
* Bytecode execution
* Ledger determinism, essential for consensus

### Function definitions
Named expressions can be added to the library:
```
func <function name> : <expression>
```
Example:
```
func lessOrEqualThan : or(lessThan($0,$1), equal($0,$1))
```
This defines a two-parameter function for the $\le$ relation.

In the library, the definition of a function takes the form of a _function descriptor_, serialized as JSON. A descriptor includes:
```json
{
  "sym":        "<function name>",
  "description":"<free description of the purpose>",
  "funCode":    "<function code (numeric ID)>",
  "numArgs":    "<number of parameters; -1 means a variadic function>",
  "embeddedAs": "<name of the hardcoded function — embedded functions only>",
  "short":      "<true for a short call code (funCode up to 63)>",
  "source":     "<source of the expression — extended (non-embedded) functions>",
  "bytecode":   "<hex-encoded compiled bytecode — extended functions>",
  "immutable":  "<true to prevent modification of the function in library upgrades>"
}
```
For example, the descriptor of the `lessOrEqualThan` function above is:
```json
{
  "sym": "lessOrEqualThan",
  "description": "returns $0<=$1. Requires operands of equal length",
  "funCode": 322,
  "numArgs": 2,
  "source": "or(lessThan($0,$1),equal($0,$1))",
  "bytecode": "48421f0001130001"
}
```

### Compilation/ decompilation
Compilation **serializes** source code into bytecode using the library:
$$
code(E) = callPrefix(fn)||code(e_0)||\dots ||code(e_{n-1})
$$
The $callPrefix(fn)$ encodes the function's ID and arity (1–3 bytes).

Compilation of the source code into bytecode serves as serialization primitive. 
Compilation to bytecode only depends on the function name and number of its arguments. 
This makes **serialization of scripts independent of the function implementation and is backward compatible**. 

EasyFL toolset provides _decompilation_ of bytecode to it source form. While source of the formula is not unique, the decompilation with subsequent compilation of the bytecode will always produce original bytecode. 

Decompilation is also a **deserialization** primitive.

### Bytecode
Bytecode represents expressions as nested arrays of compiled calls. Literals are also calls, which returns constant value.

### No recursion
The library of function definitions is enforced to be without call loops. 
That makes each evaluation to be bounded by the size of the bytecode.

### Library upgradability
Library normally is fixed and immutable. However, `EasyFL` toolset supports backward compatible upgrades of the library by producing new versions of the library while keeping previous ones. 

Selected functions in the clone of the library can be modified (as long as it does not change number of arguments) and new functions can be added. Function cannot be deleted for backward compatibility of serialization.  


### Evaluation
Expressions (formulas) are evaluated in the form of the internal evaluation tree, derived from the bytecode. So, the workflow is always like this:

`<expression source> -> <bytecode> -> <evaluation tree> -> <evaluation>`.

* Evaluation is **lazy**: expressions are only evaluated if needed.
* Example: `if(concat, byte(0,1), 0x01)` will always return `0x01` and will not panic despite the fact that `byte(0,1)` will panic if evaluated in isolation.

Lazy evaluation is important in functions like `or` and `and`: arguments are evaluated one by one and evaluation stops when value is concluded. 

### Exceptions
Some expressions may trigger panics, such as `byte(0,1)` accessing an out-of-bounds index.

`fail` is a built-in function that always panics with a message. Literal `!!!msg` is a shortcut.

Standard helper function `require` is often used to enforce certain conditions:
```
func require : or($0,$1)
```

For example: `require(lessThan(uint8Bytes($0), u64/1000), !!!argument_must_be_less_than_1000)`

Evaluation engines like `EvalFromBinary` in Go must handle these exceptions and mark the transaction as invalid.

### Examples
* `if($0, $2, $1)` → evaluates to `$2` if `$0` is `true`, else `$1`
* `concat($0, $0, $0, $0)` repeats the only argument 4 times.

In Go:

```go
ret, err := easyfl.EvalFromSource(nil, "concat($1,$0)", []byte{222}, []byte{111})
```
will compile the source to the bytecode form, will evaluate it with provided arguments and will return reversed slice:
```go
[]byte{111,222}
```

## Platform independence
EasyFL compiler, interpreter and other tools can be implemented on any language and run on any platform.

This equips EasyFL-constrained data structures with fully platform-independent serialization/deserialization and semantical validation layer. 