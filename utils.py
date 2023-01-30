import re

dictionary = [
    'النَّجْدَيْنِ', 'الْبَلَدِ', 'الْإِنْسانَ', 'الْعَقَبَةُ', 'الصَّبْرِ', 'الْمَرْحَمَةِ', 'الْمَيْمَنَةِ', 'الْعَقَبَةَ', 'الْمَشْأَمَةِ',
    'لَمْ', 'لَا', 'لَنْ',
    'لَّ', 'بِ', 'فِي', 'عَلَى', 'مِنَ', 'عَلَيْ',
    'وَ', 'أَوْ', 'ثُمَّ',
    'لَ',
    'قَدْ',
    'هَذَا', 'أُوْلَئِكَ',
    'مَا', 'الَّذِينَ',
    'فَ',
    'أَ', 'مَا',
    'يَقُولُ', 'أَهْلَكْ', 'يَحْسَبُ', 'يَرَ', 'نَجْعَل', 'هَدَيْ', 'أُقْسِمُ', 'وَلَدَ', 'خَلَقْ', 'يَقْدِرَ', 'اقْتَحَمَ', 'أَدْرَا', ' كَانَ', 'آمَنُ', 'تَوَاصَ', 'كَفَرُ',
    'مَالًا', 'لُبَداً', 'أَحَدٌ', 'عَيْنَيْنِ', 'لِسَانًا', 'شَفَتَيْنِ', 'حِلٌّ', 'وَالِدٍ', 'كَبَدٍ', 'فَكُّ', 'رَقَبَةٍ', 'إِطْعَامٌ', 'يَوْمٍ', 'ذِي', 'مَسْغَبَةٍ', 'يَتِيمًا', 'ذَا', 'مَقْرَبَةٍ', ' مِسْكِينًا', 'مَتْرَبَةٍ', 'أَصْحَابُ', 'آيَاتِ', 'مُّؤْصَدَةٌ', 'نَارٌ',
    'هُمْ',
    'تُ', 'هُ', 'نَا', 'أَنْتَ', 'وا', 'وْا', 'هِمْ', 'كَ', 'هِ',
    'أَنْ']

correct_verses_list = [['لَا أُقْسِمُ بِ هَذَا الْبَلَدِ ', '1'], 
[' وَ أَنْتَ حِلٌّ بِ هَذَا الْبَلَدِ ', '2'], 
[' وَوَالِدٍ وَمَا وَلَدَ ', '3'], 
[' لَقَدْ خَلَقْنَا الْإِنْسانَ فِي كَبَدٍ ', '4'], 
[' أَيَحْسَبُ أَنْ لَنْ يَقْدِرَ عَلَيْهِ أَحَدٌ ', '5'], 
[' يَقُولُ أَهْلَكْتُ مَالًا لُبَداً ', '6'], 
[' أَيَحْسَبُ أَنْ لَمْ يَرَهُ أَحَدٌ ', '7'], 
[' أَلَمْ نَجْعَل لَّهُ عَيْنَيْنِ ', '8'], 
[' وَلِسَانًا وَشَفَتَيْنِ ', '9'], 
[' وَهَدَيْنَاهُ النَّجْدَيْنِ ', '10'], 
[' فَلَا اقْتَحَمَ الْعَقَبَةَ ', '11'], 
[' وَمَا أَدْرَاكَ مَا الْعَقَبَةُ ', '12'], 
[' فَكُّ رَقَبَةٍ ', '13'], 
[' أَوْ إِطْعَامٌ فِي يَوْمٍ ذِي مَسْغَبَةٍ ', '14'], 
[' يَتِيمًا ذَا مَقْرَبَةٍ ', '15'], 
[' أَوْ مِسْكِينًا ذَا مَتْرَبَةٍ ', '16'], 
[' ثُمَّ كَانَ مِنَ الَّذِينَ آمَنُوا وَتَوَاصَوْا بِالصَّبْرِ وَتَوَاصَوْا بِالْمَرْحَمَةِ ', '17'], 
[' أُوْلَئِكَ أَصْحَابُ الْمَيْمَنَةِ ', '18'], 
[' وَالَّذِينَ كَفَرُوا بِآيَاتِنَا هُمْ أَصْحَابُ الْمَشْأَمَةِ ', '19'], 
[' عَلَيْهِمْ نَارٌ مُّؤْصَدَةٌ ', '20']]

translated_verses_list=[
    "I do swear by this city ˹of Mecca˺",
    "even though you ˹O Prophet˺ are subject to abuse in this city",
    "and by every parent and ˹their˺ child",
    "Indeed, We have created humankind in ˹constant˺ struggle.",
    'Do they think that no one has power over them?',
    'boasting, “I have wasted enormous wealth!”',
    'Do they think that no one sees them?',
    'Have We not given them two eyes?',
    'a tongue, and two lips?',
    'and shown them the two ways ˹of right and wrong˺?',
    'If only they had attempted the challenging path ˹of goodness instead˺!',
    'And what will make you realize what ˹attempting˺ the challenging path is?',
    'It is to free a slave.',
    'or to give food in times of famine.',
    "to an orphaned relative.",
    "or to a poor person in distress.",
    'and—above all—to be one of those who have faith and urge each other to perseverance and urge each other to compassion.',
    'These are the people of the right.',
    'As for those who deny Our signs, they are the people of the left.',
    'The Fire will be sealed over them.'
]

# formats input into list of [verse, number]
def formatter(lines):
    split_lines =re.split('(\d+)', lines)
    split_lines = [item.replace('\n', ' ') for item in split_lines]
    verses = []
    for i in range(0, len(split_lines),2):
        verses.append(split_lines[i:i+2])
    return verses