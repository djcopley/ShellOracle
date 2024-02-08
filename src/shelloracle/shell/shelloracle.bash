__shelloracle__() {
  local output
  output=$(python3 -m shelloracle) || return
  READLINE_LINE=${output#*$'\t'}
  if [[ -z "$READLINE_POINT" ]]; then
    echo "$READLINE_LINE"
  else
    READLINE_POINT=0x7fffffff
  fi
}

if (( BASH_VERSINFO[0] < 4 )); then
  bind -m emacs-standard '"\C-f": "\C-e \C-u\C-y\ey\C-u"$(__shelloracle__)"\e\C-e\er"'
  bind -m vi-command '"\C-f": "\C-z\C-r\C-z"'
  bind -m vi-insert '"\C-f": "\C-z\C-r\C-z"'
else
  bind -m emacs-standard -x '"\C-f": __shelloracle__'
  bind -m vi-command -x '"\C-f": __shelloracle__'
  bind -m vi-insert -x '"\C-f": __shelloracle__'
fi
