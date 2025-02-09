function __shelloracle__
    set -l output (shor)
    if test $status -ne 0
        return $status
    end
    commandline -r -- $output
end

bind \cf __shelloracle__
