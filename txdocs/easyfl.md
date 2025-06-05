
# EasyFL: a simple functional language

## Introduction
**EasyFL** stands for **Easy** **F**unctional **L**anguage. It is a very simple, a LISP-like functional programming language, without recursion and `eval` function though. It is extendable and is based on platform-independent bytecode.

**Note, that _EasyFL_ is not a rich programming environment or universal programming language, or even, a smart contract language. It is a low level tool intended for scripting validity constraints of the UTXO transactions at the lowest, byte level. One may see it as an assembly language of the Proxima UTXO transactions. EasyFL is equivalent to the stack-based VMs, used in Bitcoin and elsewhere, however it offers a pure functional syntax and semantics, which we see more convenient and verifiable.**  

The *EasyFL* compiler, a core library and runtime engine are available at the [EasyFL repository](https://github.com/lunfardo314/easyfl). _EasyFL_ is the scripting language used in the Proxima UTXO transactions.  

The requirements for such a language and the endgine are:
* minimalism and maximum simplicity of the language and of the runtime semantics
* easy formally verifiable, and, potentially, efficiently zk-provable
* as tiny bytecode as possible
* determinism of the compiler and of interpretation
* source easily readable by humans
* minimal set of hardcoded primitives (_op-codes_)
* extendable with higher level concepts by the means of the language itself 
* extendable standard library
* bounded nature of the computational model, no need for gas budgeting, non-Turing complete verification-oriented, etc. This is closely related to simplicity and other the requirements above.

The models such as *Bitcoin Script*, *Algorand VM* and the likes meet most of the requirements, exept verifiability, understandability and minimalism. To make language understandable, verifiable and minimalistic we choose path of the pure functional style of it.

Example: the following EasyFL expression interpreted in the context of a transaction states that the length of the unlock block for the consumed output must be 96 bytes long:

```go
equal(len(selfUnlockBlock), u64/96)
```

In the above we assume the following:
* expression is evaluated for the particular consumed UTXO
* function `selfUnlockBlock` returns the bytes of the unlock block corresponding to the consumed UTXO. If it does not exist, the evaluation panics

## The language

### Data types
The only data type in *EasyFL* is *byte array* (aka *byte slice*). It can be empty (zero length).

The only type of EasyFL statement has form and semantics of a function call, that take *byte arrays* as call arguments and returns a *byte array* as a result.

Wherever appropriate, the empty byte array is interpreted as `false` value . Any non-empty value is interpreted as `true`.

### Expressions
*EastFL source* is any ASCII text with line delimiters.

Any text in the line from symbols `//` to the end of line are comments. They have no effect on the execution.

*Expression* is a text where all *space* symbols (`\n`, `\r`, `\t`, ` `) are ignored. The source code of the `expression `is parsed to a sequence of `lexems`. A `lexem` is an ASCII string between `delimiters`.

The `delimiters` are `(`, `)` and `,`.

Source of the `expression` has the following form of the function `call`:

`<expression> ::= <funcName>[(<call args>)] || <literal>`

Here with meta symbols `[]` we enclose optional part. `<call args>` is a comma-delimited list of `<expression>`-s, which can be missing.

`<funName>` is a name of the function which is present in the library or is a `literal`.
`literals` are distinguished from library function names by syntax (see below).

Each function in the library defines its *arity*, the number of parameters it takes.

Each function can have `arity` from 0 to 7, i.e. the function can take from none to 7 call arguments. Embedded library functions, if defined so, can take any number of arguments from 0 to 7.

If function `fun` takes 0 arguments, the expressions `fun` and `fun()` are equivalent. For example `selfUnlockParameters` is equivalent to `selfUnlockParameters()` and is a function call with no arguments, it returns a value, a byte array, upon evaluation.

### Literals
By `zero-prefix-trimmed` integers we understand big-endian byte representations of integers with all leading zero bytes trimmed. For example integer `1025` will be represented as 2 bytes `0201`, while $2^{16}+3$ will be represented by `010003`. 
Zero will be represented as an empty (zero length) byte array.

Each `literals`  are constants, i.e. expressions which always returns the same value. There are the following types of literals:
* decimal number between `0` and `255`, it is a 1-byte array with the respective value. For example `0`, `42` are correct `constant literals` while `1337` is not;
* a literal with the prefix `0x` is interpreted as a hexadecimal representation of the `byte array` of length, less than 127 bytes. For example `0xff0102` is a 3-byte array, while `0x123` is incorrect;
* literal with the prefix `u16/` is a function which returns 2-byte array, a *big-endian* representation of the tail after the prefix;
* literal with the prefix `u32/` is a function which returns 4-byte array, a *big-endian* representation of the tail after the prefix;
* literal with the prefix `u64/` is a function which returns 8-byte array, a *big-endian* representation of the tail after the prefix;
* literal with the prefix `z16/` is a function which returns zero-prefix-trimmed value of `u16`, i.e. up to 2 bytes;
* literal with the prefix `z32/` is a function which returns zero-prefix-trimmed value of `u32`, i.e. up to 4 bytes;
* literal with the prefix `z64/` is a function which returns zero-prefix-trimmed value of `u64`, i.e. up to 8 bytes;
* the literal which starts with `!!!` is a call to embedded `fail` function. The tail after the `!!!` prefix is interpreted as an inline error message in the `panic` statement. For example, when and if expression `!!!not_enough_storage_deposit` is evaluated, it results in failure of the whole script with the message `not enough storage deposit` (the `_` are replaced with spaces)
* the literal which starts with `x/` represents inline *EasyFL* formula in its canonic bytecode form, represented as hexadecimal. For example literal expression `x/10856369616f21` is equivalent to the literal `!!!ciao!`
* the literal which start with the prefix `#` returns 1 or 2-byte long array with encoded binary code of the function with the name in the postfix. For example expression `#concat` is equivalent to the literal of the `concat` function code and `#address25519` is a code of the `address25519` function. The `#` literal is used in bytecode manipulations: a script for example can check is some specified bytecode indeed represents `address25519` siglock constraint.

### Examples of closed expressions
Below we will introduce EasyFL formulas with open parameters, the library and what is context of evaluation. 

Meanwhile, for simplicity, we will provide examples of closed (without parameters) EasyFL expressions whcih have obvious semantics of evaluation and always evaluates to the same value in the context.  

The standard library contains embedded functions. Here are some of them: `fail`, `concat`, `slice`, `byte`, `tail`, `equal`, `if`, `and`, `or`, `not`, `len8` and many others. The following are valid expressions:

* `0x` and `z32/0`returns empty slice
* `slice(0x01020304,1,2)` takes slice of bytes from 1 to 2 (inclusive) from its 3rd element, i.e. it returns 2-byte long array `0x0203`.
* `slice(0x0102,1,1)` takes the element with index 0, return 1-byte long array `0x02`.
* `byte(0x0102, 1)` is an equivalent to the above
* `concat(1, 5)` is equivalent to `0x0105` and is equivalent to `u16/21`, which is equivalent to `z64/21`
* `concat` (without arguments) always returns empty slice. This is equivalent to `false` and to `0x`.
* `equal(concat(1, 5), 0x01ff)` always returns empty slice, i.e. `false`
* `if(0, u16/31415, u32/271828` will always evaluate to 2-byte slice `u16/31415`
* `or` will always return empty slice `false`
* `and` will always return non-empty slice `true`, undefined which one exactly

### Parameters of the expression
An `expression` can use special function calls `$0`, `$1` ... `$7`.  They represent *open parameters of the expression*. Parameters of the expression will be instantiated with values whenever `expression` is evaluated, i.e. whenever it calls the corresponding `$i` function. The use of the parameter `$i` in the expression means that at least `i+1` arguments must be supplied when `expression` is evaluated.

For example expression `concat($0,$1)` will evaluate to the concatenation of the arguments, provided by the call context and `concat(byte($0,1), byte($0,0), tail($0,2)))` will return byte array with swapped first two bytes. 

Expression parameters can be used at any level of the expression, i.e. `not(not(not(not($0))))` is a correct expression, it will require 1 argument.

Expression `or($3)` will return 4th argument, however all 4 must be supplied in the call context, only first 3 won't be used.

## Library of definition. Compilation. Execution
EasyFL library defines a correspondence between function names, function codes and function descriptors.
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

[YAML link](library.yaml)

### Base library in YAML








### Evaluation
Expressions are evaluated in the form of the internal evaluation tree, derived from the bytecode. So, the workflow is always like this:

`<expression source> -> <canonical bytecode> -> <evaluation tree> -> <evaluation>`.

The engine (function `EvalExpression`) is using **lazy evaluation**. It means argument expression is only evaluated when and if it is needed for the evaluation of the context where it is used as a parameter. For example, the expression:
`if(concat, byte(0,1), 0x01)` will never panic even if `byte(0,1)` always panics (see *Exceptions* below). It is because `concat` always returns `false` and `if` function always evaluates only one of two branches.


### Exceptions
Evaluation of the expression may fail with the panic. For example, expression `byte(0,1)` will always panic, because it tries to take a byte with index `1` from the 1-byte array `[0]`.

The embedded function `fail` always panics with its only argument interpreted as the error message/string. The `!!!<msg>` is a shortcut literal of the `fail` function call.

The evaluation engine (the Go function `EvalFromBinary`) does not process exceptions. The transaction validation context, which invokes the evaluation engine, must intercept panic and treat transaction as invalid.



### Examples 2
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

### Extension of the library
The semantics of execution of the expressions depends on the functions itself. The runtime environment of *EasyFL* assumes `the library`, which contains all function definitions, available for the evaluation engine. For the UTXO transaction validation, the library must be the same on each node.

There are two types of functions: `embedded` and `extended`.

#### Embedded functions
`Embedded` functions are hardcoded executable code of the host environment, for example Go code. They are defined by `name`, `arity` and the Go function to be executed (or other language environment). Example of embedding:

Function with variable number of arguments.
```go
EmbedShort("concat", -1, func (par *CallParams) []byte {
	var buf bytes.Buffer
	for i := byte(0); i < par.Arity(); i++ {
		buf.Write(par.Arg(i))
	}
	return buf.Bytes()
})
```

Function with fixed `arity` 3.
```go
EmbedLong("validSignatureED25519", 3, func(ctx *CallParams) []byte {
	msg := ctx.Arg(0)
	signature := ctx.Arg(1)
	pubKey := ctx.Arg(2)
	if ed25519.Verify(pubKey, msg, signature) {
		return []byte{0xff} // anything not nil is true
	}
	return nil
})
```

Embedded functions usually have a very simple and clear semantics. They usually contains very core functions or very complicated, such as cryptography.

The embedded code accesses arguments of the call through provided context of type `ctx *CallParams`. The global data structure being validated, such as UTXO transaction, is accessed as `ctx.DataContext()`. This way embedded code have access to the whole data context it is validating.

Notably, the embedded code is running any code on the host environment, so it is not restricted to the *non-Turing equivalence*, i.e. it may run any loops and queries on the provided data context. This is up to the developer of the embedded code with all the consequences, because embedded code is out of control of the transaction validation context.

Note, that embedded code is always provided by the node developer. Meanwhile, the transaction production environment can only provide *EasyFL* expessions, bytecode or source and they are protected by the bounded nature of the computation model (see *Extended functions* below).

So, the embedded functions can also contain calls to other, more complicated, environmens, VMs and interpreters, such as EVM or Wasm. **Function embedding is a natural point where ledger protocol may be extended.**

The call context `ctx *CallParams` provides access to parameters of the call and access to the data structure the expression is validating. In the UTXO case the data structure is the UTXO transaction itself.

#### Extended functions

Extended funtions are defined by expression in the source form. For example:

```go
	Extend("nil", "or")
	Extend("false", "or")
	Extend("true", "and")
	Extend("lessOrEqualThan", "or(lessThan($0,$1),equal($0,$1))")	
```
adds functions `nil` (0 parameters, call `or()` always returns `false/nil` and `and` always returns some non-empty slice, interpreted as `true` ) and `lessOrEqualThan` (2 parameters) as an expressions to the library. The `Extend` call compiles expression and prepares it for evaluation. It automatically calculates `arity` of the function as `i+1`, where `$i` is the largest number of the parameter.

The strict requirement is: **any function referenced in the expression must already exist in the library**. This restriction makes the *EasyFL* compiler extemely simple and **prevents recursive definitions of functions**. It also and makes the computational model of *EasyFL* expressions **non-Turing equivalent**, just as intended.

#### Extension with many functions
*EasyFL* compiler provides following notation to extend library with many function definition. It is usefull extend library with more complex transaction constraints.

Each library extension of this kind has a form:

`func <function name>: <expression>`

In the source may be many these function definitions.

#### Local libraries
The *EasyFL* compiled and runtime support embedable libraries, so called **local libraries**. The *local library* is a collection of *EasyFL* functions compiled into the canonical bytecode format. Another  *EasyFL* function can call (invoke) an *EasyFL* function from the compiled local library, which is provided as parameter. This feature enables use cases, for example when constraint requires to know another unocking script to unlock the first one. Example may be hash-locking the output and to unlock it we must provide script as pre-image of the hash.

## Bigger example: ED25519 sig lock constraint
The following is an example of a *sigLocED25519* constraint, which only allows transaction to be valid, if the output is unlocked by the valid ED25519 signature of the transaction essence or points to another input, which contains a valid signature verifiable with  the same address.

The source code is taken from the `EasyUTXO` PoC ledger implementation. It is provided here to demonstrate expressiveness of the language.

```go
// ED25519 address constraint wraps 32 bytes address, the blake2b hash of the public key
// For example expression 'addressED25519(0x010203040506..)' used as constraint in the output makes 
// the output unlockable only with the presence of signature correspomding 
// to the address '0x010203040506..'

// $0 = address data 32 bytes
// $1 = signature
// $2 = public key
// return true if transaction essence signature is valid for the address
func unlockedWithSigED25519: and(
	equal($0, blake2b($2)), 		       // address in the address data must be equal to the hash of the public key
	validSignatureED25519(txEssenceBytes, $1, $2)
)

// 'unlockedByReference'' specifies validation of the input unlock with the reference.
// The referenced constraint must be exactly the same  but with strictly lesser index.
// This prevents from cycles and forces some other unlock mechanism up in the list of outputs
func unlockedByReference: and(
	lessThan(selfUnlockParameters, selfOutputIndex),              // unlock parameter must point to another input with 
							                                      // strictly smaller index. This prevents reference cycles	
	equal(self, consumedLockByOutputIndex(selfUnlockParameters))  // the referenced constraint bytes must be equal to the self constraint bytes
)

// if it is 'produced' invocation context (constraint invoked in the input), only size of the address is checked
// Otherwise the first will check first condition if it is unlocked by reference, otherwise checks unlocking signature
// Second condition not evaluated if the first is true
// $0 - ED25519 address, 32 byte blake2b hash of the public key
func addressED25519: and(
	equal(selfBlockIndex,2), // locks must be at block #2
	or(
		and(
			selfIsProducedOutput, 
			equal(len8($0), 32) 
		),
		and(
			selfIsConsumedOutput, 
			or(
					// if it is unlocked with reference, the signature is not checked
				unlockedByReference,
					// tx signature is checked
				unlockedWithSigED25519($0, signatureED25519(txSignature), publicKeyED25519(txSignature)) 
			)
		),
		!!!addressED25519_unlock_failed
	)
)
```

