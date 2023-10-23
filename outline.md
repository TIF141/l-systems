## Outline

### `class L-system`

#### Properties
- `alphabet: None`
- `rules: {}`

#### Methods
- `add_rule({'a': 'ab'})`
  - verify that all letters exist in alphabet; else add letters
- `print_alphabet()`
  - print alphabet
- `print_rules`
  - print rules dict
- `step(initial: Str)`
  - return another string




### `class visualiser`

#### Properties

#### Methods
- `display_system(system: Lsystem, input: Str, n_steps: Int, animate=False)`
  - return graphical output (console or GUI)
- `visualise_string(mystring: Str)`
  - return output



### `class generator`
#### Properties
- `lsystem: Lsystem`

#### Methods
