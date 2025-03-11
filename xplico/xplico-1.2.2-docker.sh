#!/bin/sh

################################################################################################
# Variables
################################################################################################
OS=$(uname -r | sed -n -e 's/.*\(fc..\).*/\1/p' -e 's/.*\(el.\).*/\1/p' -e 's/.*\(amzn.\).*/\1/p')
Repository=certlifter
Member=NAME
case "$Member" in
xplico)
	Name=NAME
	Login=xplico
	Password=xplico
	Version=VERSION
	Release=RELEASE
	Port=9876
	;;
esac

case "$OS" in
fc*)
	PROGRAM=docker
	;;
el*)
	PROGRAM=podman
	;;
amzn*)
	PROGRAM=docker
	;;
esac

################################################################################################
# First check that the current user is in the docker group
################################################################################################
case "$OS" in
fc*|amzn*)
	Group=docker
	FakeGroup=test$$
	for group in $(groups) $FakeGroup
	do
		case "$group" in
		$Group)
			break
			;;
		$FakeGroup)
			echo "$USER is not a member of the group $Group - adding $USER to $Group."
			sudo usermod -a -G "$Group" "$USER"
			echo "You must logout and login to activate this new group, then run $0 again."
			;;
		esac
	done
	;;
esac

################################################################################################
# Next, check that docker is running and can find the docker image 
################################################################################################
case "$OS" in
fc*|amzn*)
	Daemon=dockerd
	if ! pidof "$Daemon" > /dev/null 2>&1; then
		echo "Docker is not running. Please start it taking into account your system proxy."
		echo "This site may be helpful: https://docs.docker.com/config/daemon/systemd/#httphttps-proxy"
		echo "Then run $0 again."
		exit 1
	fi
	;;
esac

if ! "$PROGRAM" search "$Repository" 2>&1 | grep -q "$Name"; then
	echo "Cannot find $Repository/$Name."
	echo "Check your proxy and run $0 again."
	exit 1
fi

if [[ "$1" == "start" || $# == 0 ]]; then
	################################################################################################
	# The user is in the right group, the docker daemon is running, and the correct image can be
	# found. Pull the image.
	################################################################################################
	if ! "$PROGRAM" images | sed 1d|grep -q "$Repository/$Name  *$Version-$Release "; then
		if ! "$PROGRAM" pull "$Repository/${Name}:$Version-$Release"; then
			echo "Unable to pull $Repository/${Name}:$Version-$Release. Correct the problem and run $0 again."
			exit 1
		fi
	fi

	i=0
	################################################################################################
	# Run or Start the image
	################################################################################################
	while (( i < 5 ))
	do
		State="$("$PROGRAM" ps -a | sed -n -e '/xplico/s/.* \<Up\> .*/Up/p' -e '/xplico/s/.* \<Exited\> .*/Exited/p' -e '/xplico/s/.* \<Created\> .*/Created/p')"
		case "$State" in
		Up)
			break
			;;
		Exited)
			"$PROGRAM" --log-level error start "$Name"
			sleep 5
			((i++))
			;;
		*)
			echo "Starting $Repository/${Name}:$Version-$Release"
			if ! "$PROGRAM" run -d -p ${Port}:${Port} --name "$Name" "$Repository/${Name}:$Version-$Release"; then
				echo "Could not start $Repository/${Name}:$Version-$Release.  Correct the problem and run $0 again."
				exit 1
			fi
			sleep 5
			((i++))
			;;
		esac
	done

	################################################################################################
	# All is well. Tell the user how to access Xplico.
	################################################################################################
	echo "$Name is running. To access, browse to http://localhost:${Port} and login with user $Login and password $Password"
fi

################################################################################################
# Stop the image if it is running
################################################################################################
if [[ "$1" == "stop" ]]; then
	i=0
	while (( i < 5 ))
        do
                State="$("$PROGRAM" ps -a | sed -n -e '/xplico/s/.* \<Up\> .*/Up/p' -e '/xplico/s/.* \<Exited\> .*/Exited/p' -e '/xplico/s/.* \<Created\> .*/Created/p')"
                case "$State" in
                Up)
                        "$PROGRAM" --log-level error stop "$Name"
			sleep 5
			((i++))
                        ;;
		Exited|Created)
			break
			;;
		*)
			echo "Unknown state - $State - for ${Name}:$Version-$Release"
			exit 1
			;;
		esac
	done
fi
exit 0
