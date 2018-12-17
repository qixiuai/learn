for i in {1..30}; do
    if [ ${i} -lt 10 ]; then
	wget http://web.stanford.edu/class/engr40m/slides/lecture0${i}.pdf
    else
	wget http://web.stanford.edu/class/engr40m/slides/lecture${i}.pdf
    fi
done
