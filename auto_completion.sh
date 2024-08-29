echo '_debug_sh_complete() {
    local cur_word prev_word opts
    cur_word="${COMP_WORDS[COMP_CWORD]}"
    prev_word="${COMP_WORDS[COMP_CWORD-1]}"

    case "$prev_word" in
        -f)
            opts=$(find "$(pwd)/src" -maxdepth 1 -type f -printf "%f\n")
            ;;
        *)
            opts="-f"
            ;;
    esac

    COMPREPLY=($(compgen -W "${opts}" -- "${cur_word}"))
    return 0
}

complete -F _debug_sh_complete ./debug.sh' >> ~/.bashrc

echo -e "\e[34mPlease restart your terminal or run 'source ~/.bashrc'.\e[0m"