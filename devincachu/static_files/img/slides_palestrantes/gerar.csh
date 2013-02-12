#!/bin/csh -e

foreach f ( *.jpg )
	echo "<li><img src='{{ STATIC_URL }}img/slides/${f}'></li>"
end
