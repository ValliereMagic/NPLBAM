import json
# This python file was just used to create the json for the Dog Questions. Is not actively ran.
# Its a one time used file to create the dog json.

# Create an initial list
questions = []
# Append to the list the first group and its subgroups. With its questions.
questions.append({
    "name": "Dog Information",
    "subgroups": [
        {
            "name": "Animal Basics",
            "questions": [
                {
                    "type": "text",
                    "label": "Name",
                    "name": "name",
                },
                {
                    "type": "radio",
                    "label": "Status",
                    "name": "status",
                    "answers": [
                        {
                            "name": "status_stray",
                            "label": "Stray",
                            "selected": 1,
                        },
                        {
                            "name": "status_surrender",
                            "label": "Surrender",
                            "selected": 0,
                        },
                        {
                            "name": "status_other",
                            "label": "Other",
                            "selected": 0,
                        },
                    ],
                },
                {
                    "type": "radio",
                    "label": "Sex",
                    "name": "sex",
                    "answers": [
                        {
                            "name": "sex_male",
                            "label": "Male",
                            "selected": 0,
                        },
                        {
                            "name": "sex_female",
                            "label": "Female",
                            "selected": 0,
                        },
                        {
                            "name": "sex_unknown",
                            "label": "Unknown",
                            "selected": 1,
                        },
                    ],
                },
                {
                    "type": "text",
                    "label": "Age",
                    "name": "age",
                },
                {
                    "type": "text",
                    "label": "Weight",
                    "name": "weight",
                },
                {
                    "type": "text",
                    "label": "Breed",
                    "name": "breed",
                },
                {
                    "type": "text",
                    "label": "Colour",
                    "name": "colour",
                },
                {
                    "type": "text",
                    "label": "Markings",
                    "name": "markings",
                },
            ],
        },
        {
            "name": "Medical",
            "questions": [
                {
                    "type": "radio",
                    "label": "Sterilized",
                    "name": "sterilized",
                    "answers": [
                        {
                            "name": "sterilized_yes",
                            "label": "Yes",
                            "selected": 0,
                        },
                        {
                            "name": "sterilized_no",
                            "label": "No",
                            "selected": 0,
                        },
                        {
                            "name": "sterilized_unknown",
                            "label": "Unknown",
                            "selected": 1,
                        },
                    ],
                },
                {
                    "type": "radio",
                    "label": "Microchip",
                    "name": "microchip",
                    "answers": [
                        {
                            "name": "microchip_yes",
                            "label": "Yes",
                            "selected": 0,
                        },
                        {
                            "name": "microchip_no",
                            "label": "No",
                            "selected": 0,
                        },
                        {
                            "name": "microchip_unknown",
                            "label": "Unknown",
                            "selected": 1,
                        },
                    ],
                },
                {
                    "type": "radio",
                    "label": "In Heat",
                    "name": "inheat",
                    "answers": [
                        {
                            "name": "inheat_yes",
                            "label": "Yes",
                            "selected": 0,
                        },
                        {
                            "name": "inheat_no",
                            "label": "No",
                            "selected": 0,
                        },
                        {
                            "name": "inheat_unknown",
                            "label": "Unknown",
                            "selected": 1,
                        },
                    ],
                },
                {
                    "type": "radio",
                    "label": "Visible Parasites",
                    "name": "parasites",
                    "answers": [
                        {
                            "name": "parasites_yes",
                            "label": "Yes",
                            "selected": 0,
                        },
                        {
                            "name": "parasites_no",
                            "label": "No",
                            "selected": 0,
                        },
                        {
                            "name": "parasites_unknown",
                            "label": "Unknown",
                            "selected": 1,
                        },
                    ],
                },
                {
                    "type": "radio",
                    "label": "Stool",
                    "name": "stool",
                    "answers": [
                        {
                            "name": "stool_normal",
                            "label": "Normal",
                            "selected": 0,
                        },
                        {
                            "name": "stool_soft",
                            "label": "Soft",
                            "selected": 0,
                        },
                        {
                            "name": "stool_diarrhea",
                            "label": "Diarrhea",
                            "selected": 0,
                        },
                        {
                            "name": "stool_unknown",
                            "label": "Unknown",
                            "selected": 1,
                        },
                    ],
                },
            ],
        },
    ],
})

questions.append({
    "name": "Temperment",
    "subgroups": [
        {
            "name": "Physical Contact With",
            "questions": [
                {
                    "type": "checkbox",
                    "label": "Paws",
                    "name": "paws",
                    "answers": [
                        {
                            "name": "paws_aggressive",
                            "label": "Aggressive",
                            "selected": 0,
                        },
                        {
                            "name": "paws_uneasy",
                            "label": "Uneasy",
                            "selected": 0,
                        },
                        {
                            "name": "paws_fearful",
                            "label": "Fearful",
                            "selected": 0,
                        },
                        {
                            "name": "paws_tolerant",
                            "label": "Tolerant",
                            "selected": 0,
                        },
                        {
                            "name": "paws_relaxed",
                            "label": "Relaxed",
                            "selected": 0,
                        },
                        {
                            "name": "paws_unknown",
                            "label": "Unknown",
                            "selected": 1,
                        },
                    ],
                },
                {
                    "type": "checkbox",
                    "label": "Abdomen",
                    "name": "abdomen",
                    "answers": [
                        {
                            "name": "abdomen_aggressive",
                            "label": "Aggressive",
                            "selected": 0,
                        },
                        {
                            "name": "abdomen_uneasy",
                            "label": "Uneasy",
                            "selected": 0,
                        },
                        {
                            "name": "abdomen_fearful",
                            "label": "Fearful",
                            "selected": 0,
                        },
                        {
                            "name": "abdomen_tolerant",
                            "label": "Tolerant",
                            "selected": 0,
                        },
                        {
                            "name": "abdomen_relaxed",
                            "label": "Relaxed",
                            "selected": 0,
                        },
                        {
                            "name": "abdomen_unknown",
                            "label": "Unknown",
                            "selected": 1,
                        },
                    ],
                },
                {
                    "type": "checkbox",
                    "label": "Face",
                    "name": "face",
                    "answers": [
                        {
                            "name": "face_aggressive",
                            "label": "Aggressive",
                            "selected": 0,
                        },
                        {
                            "name": "face_uneasy",
                            "label": "Uneasy",
                            "selected": 0,
                        },
                        {
                            "name": "face_fearful",
                            "label": "Fearful",
                            "selected": 0,
                        },
                        {
                            "name": "face_tolerant",
                            "label": "Tolerant",
                            "selected": 0,
                        },
                        {
                            "name": "face_relaxed",
                            "label": "Relaxed",
                            "selected": 0,
                        },
                        {
                            "name": "face_unknown",
                            "label": "Unknown",
                            "selected": 1,
                        },
                    ],
                },
                {
                    "type": "checkbox",
                    "label": "Nose",
                    "name": "nose",
                    "answers": [
                        {
                            "name": "nose_aggressive",
                            "label": "Aggressive",
                            "selected": 0,
                        },
                        {
                            "name": "nose_uneasy",
                            "label": "Uneasy",
                            "selected": 0,
                        },
                        {
                            "name": "nose_fearful",
                            "label": "Fearful",
                            "selected": 0,
                        },
                        {
                            "name": "nose_tolerant",
                            "label": "Tolerant",
                            "selected": 0,
                        },
                        {
                            "name": "nose_relaxed",
                            "label": "Relaxed",
                            "selected": 0,
                        },
                        {
                            "name": "nose_unknown",
                            "label": "Unknown",
                            "selected": 1,
                        },
                    ],
                },
                {
                    "type": "checkbox",
                    "label": "Ears",
                    "name": "ears",
                    "answers": [
                        {
                            "name": "ears_aggressive",
                            "label": "Aggressive",
                            "selected": 0,
                        },
                        {
                            "name": "ears_uneasy",
                            "label": "Uneasy",
                            "selected": 0,
                        },
                        {
                            "name": "ears_fearful",
                            "label": "Fearful",
                            "selected": 0,
                        },
                        {
                            "name": "ears_tolerant",
                            "label": "Tolerant",
                            "selected": 0,
                        },
                        {
                            "name": "ears_relaxed",
                            "label": "Relaxed",
                            "selected": 0,
                        },
                        {
                            "name": "ears_unknown",
                            "label": "Unknown",
                            "selected": 1,
                        },
                    ],
                },
                {
                    "type": "checkbox",
                    "label": "Head",
                    "name": "head",
                    "answers": [
                        {
                            "name": "head_aggressive",
                            "label": "Aggressive",
                            "selected": 0,
                        },
                        {
                            "name": "head_uneasy",
                            "label": "Uneasy",
                            "selected": 0,
                        },
                        {
                            "name": "head_fearful",
                            "label": "Fearful",
                            "selected": 0,
                        },
                        {
                            "name": "head_tolerant",
                            "label": "Tolerant",
                            "selected": 0,
                        },
                        {
                            "name": "head_relaxed",
                            "label": "Relaxed",
                            "selected": 0,
                        },
                        {
                            "name": "head_unknown",
                            "label": "Unknown",
                            "selected": 1,
                        },
                    ],
                },
                {
                    "type": "checkbox",
                    "label": "Neck",
                    "name": "neck",
                    "answers": [
                        {
                            "name": "neck_aggressive",
                            "label": "Aggressive",
                            "selected": 0,
                        },
                        {
                            "name": "neck_uneasy",
                            "label": "Uneasy",
                            "selected": 0,
                        },
                        {
                            "name": "neck_fearful",
                            "label": "Fearful",
                            "selected": 0,
                        },
                        {
                            "name": "neck_tolerant",
                            "label": "Tolerant",
                            "selected": 0,
                        },
                        {
                            "name": "neck_relaxed",
                            "label": "Relaxed",
                            "selected": 0,
                        },
                        {
                            "name": "neck_unknown",
                            "label": "Unknown",
                            "selected": 1,
                        },
                    ],
                },
                {
                    "type": "checkbox",
                    "label": "Hind Quarters",
                    "name": "hind",
                    "answers": [
                        {
                            "name": "hind_aggressive",
                            "label": "Aggressive",
                            "selected": 0,
                        },
                        {
                            "name": "hind_uneasy",
                            "label": "Uneasy",
                            "selected": 0,
                        },
                        {
                            "name": "hind_fearful",
                            "label": "Fearful",
                            "selected": 0,
                        },
                        {
                            "name": "hind_tolerant",
                            "label": "Tolerant",
                            "selected": 0,
                        },
                        {
                            "name": "hind_relaxed",
                            "label": "Relaxed",
                            "selected": 0,
                        },
                        {
                            "name": "hind_unknown",
                            "label": "Unknown",
                            "selected": 1,
                        },
                    ],
                },
            ],
        },
        {
            "name": "Crated Behaviour",
            "questions": [
                {
                    "type": "radio",
                    "label": "Barking",
                    "name": "barking",
                    "answers": [
                        {
                            "name": "barking_yes",
                            "label": "Yes",
                            "selected": 0,
                        },
                        {
                            "name": "barking_no",
                            "label": "no",
                            "selected": 0,
                        },
                        {
                            "name": "barking_unknown",
                            "label": "Unknown",
                            "selected": 1,
                        },
                    ],
                },
                {
                    "type": "checkbox",
                    "label": "Greeting",
                    "name": "greeting",
                    "answers": [
                        {
                            "name": "greeting_growl",
                            "label": "Growl",
                            "selected": 0,
                        },
                        {
                            "name": "greeting_bark",
                            "label": "Bark",
                            "selected": 0,
                        },
                        {
                            "name": "greeting_fearful",
                            "label": "Fearful",
                            "selected": 0,
                        },
                        {
                            "name": "greeting_calm",
                            "label": "Calm",
                            "selected": 0,
                        },
                        {
                            "name": "greeting_excited",
                            "label": "Excited",
                            "selected": 0,
                        },
                        {
                            "name": "greeting_unknown",
                            "label": "Unknown",
                            "selected": 1,
                        },
                    ],
                },
                {
                    "type": "checkbox",
                    "label": "When Given Food",
                    "name": "food",
                    "answers": [
                        {
                            "name": "food_immediately",
                            "label": "Eats Immediately",
                            "selected": 0,
                        },
                        {
                            "name": "food_floor",
                            "label": "Eats off Floor",
                            "selected": 0,
                        },
                        {
                            "name": "food_noeat",
                            "label": "Does not Eat",
                            "selected": 0,
                        },
                        {
                            "name": "food_unknown",
                            "label": "Unknown",
                            "selected": 1,
                        },
                    ],
                },
            ],
        }
    ],
})


questions.append({
    "name": "Misc Information",
    "subgroups": [
        {
            "name": "Disposition",
            "questions": [
                {
                    "type": "checkbox",
                    "label": "Behaviour w/ dogs",
                    "name": "behaviourWithDogs",
                    "answers": [
                        {
                            "name": "behaviourWithDogs_aggressive",
                            "label": "Aggressive",
                            "selected": 0,
                        },
                        {
                            "name": "behaviourWithDogs_dominant",
                            "label": "Dominant",
                            "selected": 0,
                        },
                        {
                            "name": "behaviourWithDogs_excited",
                            "label": "Excited",
                            "selected": 0,
                        },
                        {
                            "name": "behaviourWithDogs_calm",
                            "label": "Calm",
                            "selected": 0,
                        },
                        {
                            "name": "behaviourWithDogs_submissive",
                            "label": "Submissive",
                            "selected": 0,
                        },
                        {
                            "name": "behaviourWithDogs_polite",
                            "label": "Polite",
                            "selected": 0,
                        },
                        {
                            "name": "behaviourWithDogs_playful",
                            "label": "Playful",
                            "selected": 0,
                        },


                        {
                            "name": "behaviourWithDogs_unknown",
                            "label": "Unknown",
                            "selected": 1,
                        },
                    ],
                },
                {
                    "type": "checkbox",
                    "label": "Overall Dog Disposition",
                    "name": "dispositionOverall",
                    "answers": [
                        {
                            "name": "dispositionOverall_aggressive",
                            "label": "Aggressive",
                            "selected": 0,
                        },
                        {
                            "name": "dispositionOverall_fearful",
                            "label": "Fearful",
                            "selected": 0,
                        },
                        {
                            "name": "dispositionOverall_shy",
                            "label": "Shy",
                            "selected": 0,
                        },
                        {
                            "name": "dispositionOverall_outgoing",
                            "label": "Outgoing",
                            "selected": 0,
                        },
                        {
                            "name": "dispositionOverall_unknown",
                            "label": "Unknown",
                            "selected": 1,
                        },
                    ],
                },
                {
                    "type": "checkbox",
                    "label": "Disposition w/ strangers",
                    "name": "dispositionStranger",
                    "answers": [
                        {
                            "name": "dispositionStranger_aggressive",
                            "label": "Aggressive",
                            "selected": 0,
                        },
                        {
                            "name": "dispositionStranger_fearful",
                            "label": "Fearful",
                            "selected": 0,
                        },
                        {
                            "name": "dispositionStranger_shy",
                            "label": "Shy",
                            "selected": 0,
                        },
                        {
                            "name": "dispositionStranger_outgoing",
                            "label": "outgoing",
                            "selected": 0,
                        },
                        {
                            "name": "dispositionStranger_unknown",
                            "label": "Unknown",
                            "selected": 1,
                        },
                    ],
                },
                {
                    "type": "checkbox",
                    "label": "In presence of food (not crated)",
                    "name": "dispositionFood",
                    "answers": [
                        {
                            "name": "dispositionFood_aggressive",
                            "label": "Aggressive",
                            "selected": 0,
                        },
                        {
                            "name": "dispositionFood_glutton",
                            "label": "Glutton",
                            "selected": 0,
                        },
                        {
                            "name": "dispositionFood_fussy",
                            "label": "Fussy",
                            "selected": 0,
                        },
                        {
                            "name": "dispositionFood_nibbler",
                            "label": "Nibbler",
                            "selected": 0,
                        },
                        {
                            "name": "dispositionFood_protective",
                            "label": "Protective",
                            "selected": 0,
                        },
                        {
                            "name": "dispositionFood_unknown",
                            "label": "Unknown",
                            "selected": 1,
                        },
                    ],
                },
                {
                    "type": "checkbox",
                    "label": "In presence of toys",
                    "name": "dispositionToy",
                    "answers": [
                        {
                            "name": "dispositionToy_selective",
                            "label": "Selective",
                            "selected": 0,
                        },
                        {
                            "name": "dispositionToy_playful",
                            "label": "Playful",
                            "selected": 0,
                        },
                        {
                            "name": "dispositionToy_destructive",
                            "label": "Destructive",
                            "selected": 0,
                        },
                        {
                            "name": "dispositionToy_possessive",
                            "label": "Possessive",
                            "selected": 0,
                        },
                        {
                            "name": "dispositionToy_uninterested",
                            "label": "Uninterested",
                            "selected": 0,
                        },
                        {
                            "name": "dispositionToy_unknown",
                            "label": "Unknown",
                            "selected": 1,
                        },
                    ],
                },
                {
                    "type": "checkbox",
                    "label": "On leash",
                    "name": "dispositionLeash",
                    "answers": [
                        {
                            "name": "dispositionLeash_pulls",
                            "label": "Pulls",
                            "selected": 0,
                        },
                        {
                            "name": "dispositionLeash_unfamiliar",
                            "label": "Unfamiliar",
                            "selected": 0,
                        },
                        {
                            "name": "dispositionLeash_polite",
                            "label": "Polite",
                            "selected": 0,
                        },
                        {
                            "name": "dispositionLeash_chews",
                            "label": "Chews",
                            "selected": 0,
                        },
                        {
                            "name": "dispositionLeash_unknown",
                            "label": "Unknown",
                            "selected": 1,
                        },
                    ],
                },
                {
                    "type": "checkbox",
                    "label": "Known Commands",
                    "name": "commands",
                    "answers": [
                        {
                            "name": "commands_sit",
                            "label": "Sit",
                            "selected": 0,
                        },
                        {
                            "name": "commands_paw",
                            "label": "Paw",
                            "selected": 0,
                        },
                        {
                            "name": "commands_stay",
                            "label": "Stay",
                            "selected": 0,
                        },
                        {
                            "name": "commands_unknown",
                            "label": "Unknown",
                            "selected": 1,
                        },
                    ],
                },
                {
                    "type": "radio",
                    "label": "Is Dog Vocal",
                    "name": "vocal",
                    "answers": [
                        {
                            "name": "vocal_never",
                            "label": "Never",
                            "selected": 0,
                        },
                        {
                            "name": "vocal_hardly",
                            "label": "Hardly",
                            "selected": 0,
                        },
                        {
                            "name": "vocal_often",
                            "label": "Often",
                            "selected": 0,
                        },
                        {
                            "name": "vocal_constantly",
                            "label": "Constantly",
                            "selected": 0,
                        },
                        {
                            "name": "vocal_unknown",
                            "label": "Unknown",
                            "selected": 1,
                        },
                    ],
                },
            ],
        },
    ],
},)


# Completed Below
questions.append({
    "name": "Visual Health",
    "subgroups": [
        {
            "name": "Visual Inspection of",
            "questions": [
            ],
        },
    ],
},)

for item in ["face", "nose", "teeth", "ears", "eyes", "neck", "abdomen", "tail", "legs", "paws", "nails", "skin", "coat", "other"]:
    questions[3]["subgroups"][0]["questions"].append(
        {
            "type": "text",
            "label": item.capitalize(),
            "name": "visual_" + item,
        }
    )


questions.append({
    "name": "Additional Information",
    "subgroups": [
        {
            "name": "Notes",
            "questions": [
                {
                    "type": "textarea",
                    "label": "Vet Notes",
                    "name": "vet",
                },
                {
                    "type": "textarea",
                    "label": "Additional Notes",
                    "name": "notes",
                },
            ],
        },
    ],
},)

# Dump the list into a json called dog_questions.
with open('dog_questions.json', 'w') as outfile:
    json.dump(questions, outfile)
