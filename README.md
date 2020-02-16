# Inspiration
A fundamental limitation of today's authentication systems is that they require users to authenticate themselves manually. 
Instead, we invision a zero-login authentication system that is ultra secure yet requires no user input, using our proposed GaitKeeper system. 

# What it does
The GaitKeeper is an authentication service that provides a user trust score without user interaction.
GaitKeeper achieves secure and interactionless authentication by learning a user's unique _gait_ and combining it with user device history.
In this way, GaitKeeper can determine whether if a user is truly who they claim to be including when a user's device is compromised.

# How we built it
There are three parts to the GaitKeeper service:
1. A client side service that continually runs on an user's device to model their behavior and carry out authentication.
2. A backend server that collects user gait behavior and cotinually runs a ML model to update and monitor this behavior.
3. A reporting portal that allows users and admins to view recent changes to their Heimdall Score.

# Challenges we ran into
A grand challenge in achieving this interactionless authentication system is that there is no one metric that can identify a user. 
GaitKeeper solves this challenge by leveraging multitudes of sensor data from users' smartphones to model the corresponding the user behaviour and there by identifying the user identity.   
