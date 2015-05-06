"""
	Extracts keywods from a corpus of lyrics
"""

from candidate.candidate import generate_candidates
import pdb

lyrics = """
i'mma make you beg, i'mma make you beg for it i'mma make you beg, i'mma make you beg... pulled up looking picture perfect, baby high price, but i'm worth it, baby can't play with ya, i've been busy workin', baby gettin' faded in the european, swervin', ayy look, describe iggy groundbreaking what the word is hit the stage, ass shakin' like i'm nervous when in new york, i be parkin' right on madison this ain't no accident, i'm killing 'em on purpose i-g-g... why did she just have to do it baby ride with me, fly living, there ain't nothing to it and my waist slim, ass fat, you gotta have it get my bake on, cake long, that's automatic i know you like the way i turn it on i'm out here with my friends i'mma make you beg, i'mma make you beg for it if you don't do this right, you're going home alone i guess you'll have to beg i'mma make you beg, i'mma make you beg for it p-p-p-pussy power, pay me by the hour i need me a braveheart, can't deal with a coward i tell him if he ain't ballin', he should hit the showers if i pick you, you lucky, baby, this money ours all yellow gold on me, like i'm trinidad (james) sittin' drop top, wondering where the ceiling's at i know my old thang wanna bring the feeling back but i got a new thang, baby, i ain't feeling that now iggy iggy iggy, can't you see? that everybody wanna put they hands on me see i be on this money while your man on me and i need another hand with all these bands on me, wait get up out my face like who d'you think you are? talking all this trash like blah-de-blah-de-blah (oh ay oh) nuh-uh (oh ay oh) nuh-uh (oh ay oh) get up out my face like who d'you think you are? make me wanna laugh like har-de-har-de-har (oh ay oh) nuh-uh (oh ay oh) nuh-uh got you hooked boy, i'm like a drug if you want my love better smoke it up (make you beg for it, i'mma make you beg for it) you can look, boy, but don't you touch if you want my love make me give a fuck (make you beg for it, i'mma make you beg for it)merde alors! i mean i don't believe this! you are going to turn down a pussy like this? staring you smack in your face no man can turn down this pussy (will you stop it?) i don't know any man that can refuse this pussy (will you stop saying pussy? people are eating in here) pussy, pussy, pussy, puss-y! pussy, puss-puss, pussy! trying to find our cat where is that cat? pu$$y pu$$y pu$$y drugs iggy iggy, pussy illy wetter than 
"""

c = generate_candidates(lyrics)
pdb.set_trace()


