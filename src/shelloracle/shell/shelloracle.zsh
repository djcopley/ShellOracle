# Define the function shelloracle-widget
shelloracle-widget() {
  # Set options and suppress any error messages
  setopt localoptions noglobsubst noposixbuiltins pipefail no_aliases 2> /dev/null

  # Run the shelloracle python module and store the result in the "selected" array
  local selected=( $(SHOR_DEFAULT_PROMPT=${LBUFFER} python3 -m shelloracle) )

  # Get the return status of the last executed command
  local ret=$?

  # Reset the prompt
  zle reset-prompt

  # Set the BUFFER variable to the selected result
  BUFFER=$selected

  # Set the CURSOR position at the end of BUFFER
  CURSOR=$#BUFFER

  # Return the status
  return $ret
}

# Register the function as a ZLE widget
zle -N shelloracle-widget

# Install the ZLE widget as a keyboard shortcut Ctrl+F
bindkey '^F' shelloracle-widget