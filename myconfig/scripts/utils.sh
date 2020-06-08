#!/bin/bash

## string parser
remove_comment_and_platform() {
  # removes comments('#'), platform unmask('~'), blank lines, require lines('@require') and bashrc modification lines('@*/*')
  sed -r -e 's/#.*//' -e 's/~//' -e '/^[[:blank:]]*$/d' -e '/^[[:blank:]]*@.*/d'
}

remove_user_mask_spec() {
  # remove spec with user mask('-')
  sed -r -e 's/^[[:blank:]]*-.*//'
}

remove_custom_mark() {
  # remove user mask('-'), mask unmask('+'), and suggestion taken('&')
  sed -e 's/^[[:blank:]]*[+-]\([[:alnum:]]\+\)/\1/' -e 's/&.*//'
}
