"""
Plant disease classes and treatment information
"""

DISEASE_CLASSES = [
    "Apple___Apple_scab",
    "Apple___Black_rot",
    "Apple___Cedar_apple_rust",
    "Apple___healthy",
    "Blueberry___healthy",
    "Cherry_(including_sour)___Powdery_mildew",
    "Cherry_(including_sour)___healthy",
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
    "Corn_(maize)___Common_rust_",
    "Corn_(maize)___Northern_Leaf_Blight",
    "Corn_(maize)___healthy",
    "Grape___Black_rot",
    "Grape___Esca_(Black_Measles)",
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
    "Grape___healthy",
    "Orange___Haunglongbing_(Citrus_greening)",
    "Peach___Bacterial_spot",
    "Peach___healthy",
    "Pepper,_bell___Bacterial_spot",
    "Pepper,_bell___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Raspberry___healthy",
    "Soybean___healthy",
    "Squash___Powdery_mildew",
    "Strawberry___Leaf_scorch",
    "Strawberry___healthy",
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites Two-spotted_spider_mite",
    "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___Tomato_mosaic_virus",
    "Tomato___healthy"
]

TREATMENT_DATA = {
    "Apple___Apple_scab": {
        "description": "Apple scab is a fungal disease caused by Venturia inaequalis. It affects both leaves and fruit, causing dark, scaly lesions that can defoliate trees and deform fruit.",
        "treatment": [
            "Apply fungicide sprays containing captan, myclobutanil, or sulfur starting at green tip stage",
            "Remove and destroy all fallen leaves in autumn to reduce overwintering inoculum",
            "Prune trees to improve air circulation and reduce leaf wetness",
            "Apply dormant oil spray before bud break to smother overwintering spores",
            "Use resistant apple varieties when planting new trees"
        ],
        "prevention": [
            "Plant resistant varieties such as Liberty, Jonafree, or GoldRush",
            "Rake and dispose of fallen leaves in fall",
            "Avoid overhead irrigation to keep foliage dry",
            "Maintain proper tree spacing for good air circulation",
            "Apply preventive fungicide sprays during wet spring weather"
        ]
    },
    "Apple___Black_rot": {
        "description": "Black rot is a fungal disease caused by Botryosphaeria obtusa. It causes leaf spots, fruit rot, and canker formation on branches, leading to significant crop losses.",
        "treatment": [
            "Prune out all dead and diseased branches, cutting 6 inches below visible canker",
            "Remove all mummified fruit from trees and ground",
            "Apply fungicides containing captan or thiophanate-methyl during growing season",
            "Destroy all pruned material by burning or burying",
            "Apply copper-based fungicides during dormant season"
        ],
        "prevention": [
            "Remove all dead wood and mummified fruit annually",
            "Maintain tree vigor through proper fertilization and watering",
            "Avoid mechanical injuries to branches and trunk",
            "Use disease-free nursery stock when planting",
            "Practice good sanitation by removing plant debris"
        ]
    },
    "Apple___Cedar_apple_rust": {
        "description": "Cedar apple rust is a fungal disease caused by Gymnosporangium juniperi-virginianae. It requires both apple and cedar trees to complete its life cycle, causing bright orange lesions on apple leaves and fruit.",
        "treatment": [
            "Apply fungicides containing myclobutanil or propiconazole during pink to petal fall stages",
            "Remove galls from nearby cedar trees within 1-2 mile radius",
            "Prune and destroy heavily infected branches",
            "Use protective fungicide sprays at 7-10 day intervals during spring",
            "Apply sulfur-based fungicides as organic alternative"
        ],
        "prevention": [
            "Remove eastern red cedar trees within 2 miles if possible",
            "Plant rust-resistant apple varieties like Dayton, Enterprise, or Freedom",
            "Apply preventive fungicides starting at pink bud stage",
            "Avoid planting apples near cedar trees",
            "Use windbreaks to reduce spore transmission"
        ]
    },
    "Apple___healthy": {
        "description": "Your apple tree appears healthy with no visible signs of disease or pest damage. The leaves show normal coloration and structure, indicating good growing conditions.",
        "treatment": [
            "No treatment needed - continue current maintenance practices",
            "Monitor regularly for early signs of disease or pests",
            "Maintain proper watering and fertilization schedule",
            "Prune annually to maintain tree structure and air circulation",
            "Consider preventive fungicide applications in spring"
        ],
        "prevention": [
            "Continue regular monitoring and maintenance",
            "Apply dormant oil spray in late winter",
            "Maintain proper tree spacing for air circulation",
            "Practice good sanitation by removing fallen leaves",
            "Schedule annual pruning during dormant season"
        ]
    },
    "Blueberry___healthy": {
        "description": "Your blueberry plant appears healthy with vibrant green foliage and no visible signs of disease or pest damage.",
        "treatment": [
            "No treatment needed - continue current care practices",
            "Maintain acidic soil pH between 4.5-5.5",
            "Provide consistent moisture throughout growing season",
            "Apply mulch to retain moisture and suppress weeds",
            "Fertilize with acid-loving plant fertilizer in early spring"
        ],
        "prevention": [
            "Plant resistant varieties suited to your climate",
            "Ensure proper soil drainage and acidity",
            "Prune annually to remove old canes and improve air flow",
            "Use bird netting to protect fruit",
            "Monitor for common pests like blueberry maggot and mites"
        ]
    },
    "Cherry_(including_sour)___Powdery_mildew": {
        "description": "Powdery mildew is a fungal disease that appears as white, powdery growth on leaves, shoots, and fruit. It thrives in warm, dry conditions with high humidity.",
        "treatment": [
            "Apply fungicides containing sulfur, myclobutanil, or trifloxystrobin",
            "Remove and destroy severely infected leaves and branches",
            "Improve air circulation through proper pruning",
            "Apply neem oil as organic fungicide option",
            "Avoid overhead watering to reduce humidity around plants"
        ],
        "prevention": [
            "Plant resistant cherry varieties",
            "Provide adequate spacing for air circulation",
            "Avoid excessive nitrogen fertilization",
            "Remove and destroy fallen leaves in autumn",
            "Apply preventive sulfur sprays during warm, humid weather"
        ]
    },
    "Cherry_(including_sour)___healthy": {
        "description": "Your cherry tree appears healthy with no visible signs of disease or pest damage. Leaves show normal coloration and growth pattern.",
        "treatment": [
            "No treatment needed - continue current maintenance",
            "Monitor for common cherry pests like aphids and fruit flies",
            "Maintain regular watering schedule",
            "Apply balanced fertilizer in early spring",
            "Prune annually during dormant season"
        ],
        "prevention": [
            "Continue regular monitoring and care",
            "Apply dormant oil spray in late winter",
            "Use bird netting to protect fruit",
            "Maintain good air circulation through proper pruning",
            "Remove any fallen fruit or leaves promptly"
        ]
    },
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "description": "Gray leaf spot is a fungal disease caused by Cercospora zeae-maydis. It produces rectangular, gray to tan lesions between leaf veins that can merge and kill entire leaves.",
        "treatment": [
            "Apply fungicides containing pyraclostrobin, azoxystrobin, or trifloxystrobin",
            "Use foliar fungicides at first sign of disease or during silking stage",
            "Rotate crops to reduce pathogen buildup in soil",
            "Remove and destroy infected plant debris after harvest",
            "Consider multiple fungicide applications in severe cases"
        ],
        "prevention": [
            "Plant resistant corn hybrids with genetic tolerance",
            "Rotate crops with non-host plants for 1-2 years",
            "Use tillage to bury infected residue",
            "Avoid late planting which increases disease severity",
            "Maintain balanced soil fertility"
        ]
    },
    "Corn_(maize)___Common_rust_": {
        "description": "Common rust is a fungal disease caused by Puccinia sorghi. It produces small, reddish-brown pustules on leaves that can reduce photosynthesis and yield.",
        "treatment": [
            "Apply foliar fungicides containing propiconazole or pyraclostrobin",
            "Treat when disease severity exceeds economic threshold",
            "Most field corn hybrids have adequate resistance",
            "Remove volunteer corn plants that can harbor the fungus",
            "Focus on sweet corn which is more susceptible"
        ],
        "prevention": [
            "Plant rust-resistant corn hybrids",
            "Avoid late planting to escape high disease pressure",
            "Control volunteer corn and weeds that may harbor the fungus",
            "Use certified disease-free seed",
            "Maintain good plant nutrition for natural resistance"
        ]
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "description": "Northern corn leaf blight is caused by the fungus Setosphaeria turcica. It produces large, cigar-shaped lesions on leaves that can significantly reduce yield.",
        "treatment": [
            "Apply fungicides containing strobilurin or triazole chemistry",
            "Time fungicide applications between tasseling and silking",
            "Use preventive fungicide sprays in high-risk fields",
            "Remove infected plant debris after harvest",
            "Consider multiple applications in severe cases"
        ],
        "prevention": [
            "Plant resistant hybrids with Ht genes",
            "Rotate crops to reduce pathogen buildup",
            "Use tillage to bury infected residue",
            "Avoid late planting",
            "Maintain balanced soil fertility"
        ]
    },
    "Corn_(maize)___healthy": {
        "description": "Your corn plant appears healthy with no visible signs of disease or pest damage. Leaves show normal green coloration and growth.",
        "treatment": [
            "No treatment needed - continue current management",
            "Monitor for common corn pests like corn borer and earworm",
            "Maintain adequate water during tasseling and grain fill",
            "Apply nitrogen fertilizer as needed based on soil tests",
            "Control weeds that compete for nutrients and water"
        ],
        "prevention": [
            "Continue regular scouting and monitoring",
            "Use integrated pest management practices",
            "Rotate crops to break pest and disease cycles",
            "Maintain proper plant population and spacing",
            "Use hybrid corn varieties suited to your area"
        ]
    },
    "Grape___Black_rot": {
        "description": "Black rot is a fungal disease caused by Guignardia bidwellii. It causes brown circular lesions on leaves and shriveled, black mummified fruit.",
        "treatment": [
            "Apply fungicides containing myclobutanil, mancozeb, or captan",
            "Begin fungicide applications when new shoots are 3-5 inches long",
            "Continue sprays every 7-14 days throughout growing season",
            "Remove and destroy all mummified fruit and infected canes",
            "Shorten sprays during dry weather but maintain coverage"
        ],
        "prevention": [
            "Plant resistant grape varieties",
            "Remove and destroy all mummified fruit after harvest",
            "Prune to improve air circulation and reduce leaf wetness",
            "Avoid overhead irrigation",
            "Use clean nursery stock when planting"
        ]
    },
    "Grape___Esca_(Black_Measles)": {
        "description": "Esca, also known as black measles, is a complex fungal disease affecting grapevines. It causes 'tiger stripe' leaf patterns and fruit spotting, leading to vine decline.",
        "treatment": [
            "No curative treatment available - prevention is key",
            "Remove and destroy severely infected vines",
            "Prune properly to avoid large wounds that serve as infection sites",
            "Apply wound protectants after pruning",
            "Use trunk renewal to replace infected cordons"
        ],
        "prevention": [
            "Avoid large pruning wounds during vine training",
            "Use proper pruning techniques and timing",
            "Apply fungicidal wound protectants after pruning",
            "Remove and destroy infected wood promptly",
            "Maintain vine vigor through proper nutrition and irrigation"
        ]
    },
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "description": "Leaf blight caused by Pseudocercospora vitis produces angular, reddish-brown lesions on leaves that can cause premature defoliation.",
        "treatment": [
            "Apply fungicides containing mancozeb, captan, or copper compounds",
            "Remove and destroy fallen infected leaves",
            "Improve air circulation through canopy management",
            "Apply sprays preventively before symptoms appear",
            "Reduce leaf wetness by avoiding overhead irrigation"
        ],
        "prevention": [
            "Remove and destroy fallen leaves after harvest",
            "Prune to improve air circulation in canopy",
            "Avoid excessive nitrogen fertilization",
            "Use drip irrigation to keep foliage dry",
            "Plant grapes in sunny, well-ventilated locations"
        ]
    },
    "Grape___healthy": {
        "description": "Your grapevine appears healthy with no visible signs of disease or pest damage. Leaves show normal green coloration and growth.",
        "treatment": [
            "No treatment needed - continue current care",
            "Monitor for common grape pests and diseases",
            "Maintain regular pruning schedule",
            "Apply appropriate fertilizers based on soil tests",
            "Ensure adequate water during fruit development"
        ],
        "prevention": [
            "Continue regular monitoring and maintenance",
            "Apply dormant sprays in late winter",
            "Use proper trellising for good air circulation",
            "Remove and destroy fallen leaves in autumn",
            "Practice good canopy management"
        ]
    },
    "Orange___Haunglongbing_(Citrus_greening)": {
        "description": "Citrus greening, also known as Huanglongbing (HLB), is a devastating bacterial disease spread by the Asian citrus psyllid. It causes yellow shoots, blotchy mottling, and bitter, misshapen fruit.",
        "treatment": [
            "No cure exists - infected trees will die within a few years",
            "Apply insecticides to control Asian citrus psyllid vectors",
            "Remove and destroy infected trees promptly to prevent spread",
            "Use antibiotic trunk injections for temporary symptom suppression",
            "Enhance tree nutrition to prolong productivity"
        ],
        "prevention": [
            "Plant certified disease-free nursery stock",
            "Control Asian citrus psyllid with regular insecticide applications",
            "Remove infected trees immediately upon detection",
            "Use physical barriers like individual protective covers on young trees",
            "Monitor regularly for psyllid presence and disease symptoms"
        ]
    },
    "Peach___Bacterial_spot": {
        "description": "Bacterial spot is caused by Xanthomonas arboricola pv. pruni. It produces angular, water-soaked lesions on leaves and sunken, cracked spots on fruit.",
        "treatment": [
            "Apply copper-based bactericides during dormant and growing seasons",
            "Use antibiotic sprays containing oxytetracycline during wet periods",
            "Prune infected branches during dry weather",
            "Remove and destroy infected plant debris",
            "Avoid overhead irrigation to reduce bacterial spread"
        ],
        "prevention": [
            "Plant resistant peach varieties like Comet, 'Jefferson', or 'Sunhigh'",
            "Avoid planting in sites with poor air drainage",
            "Use drip irrigation to keep foliage dry",
            "Maintain balanced fertilization - avoid excess nitrogen",
            "Apply preventive copper sprays in early spring"
        ]
    },
    "Peach___healthy": {
        "description": "Your peach tree appears healthy with no visible signs of disease or pest damage. Leaves show normal green coloration and growth pattern.",
        "treatment": [
            "No treatment needed - continue current maintenance",
            "Monitor for common peach pests like borers and aphids",
            "Apply dormant oil spray in late winter",
            "Maintain regular pruning for tree structure",
            "Thin fruit properly to improve quality"
        ],
        "prevention": [
            "Continue regular monitoring and care",
            "Apply preventive fungicide sprays during bloom",
            "Remove fallen leaves and fruit after harvest",
            "Maintain proper tree spacing for air circulation",
            "Practice good sanitation around the tree"
        ]
    },
    "Pepper,_bell___Bacterial_spot": {
        "description": "Bacterial spot of pepper is caused by Xanthomonas species. It produces small, water-soaked lesions on leaves that turn brown and may have yellow halos.",
        "treatment": [
            "Apply copper-based bactericides with mancozeb for improved efficacy",
            "Remove and destroy severely infected plants",
            "Avoid working in fields when foliage is wet",
            "Use disease-free certified seed or transplants",
            "Apply streptomycin or kasugamycin in severe cases"
        ],
        "prevention": [
            "Use disease-free certified seed or resistant varieties",
            "Hot-water treat seeds at 122°F for 25 minutes before planting",
            "Avoid overhead irrigation",
            "Rotate crops for 2-3 years away from peppers and tomatoes",
            "Maintain good field sanitation and remove plant debris"
        ]
    },
    "Pepper,_bell___healthy": {
        "description": "Your bell pepper plant appears healthy with no visible signs of disease or pest damage. Leaves show normal green coloration and growth.",
        "treatment": [
            "No treatment needed - continue current care",
            "Monitor for common pepper pests like aphids and flea beetles",
            "Maintain consistent soil moisture",
            "Apply balanced fertilizer as needed",
            "Provide support for heavy fruit loads"
        ],
        "prevention": [
            "Continue regular monitoring",
            "Use mulch to retain moisture and prevent soil splash",
            "Rotate crops annually to prevent disease buildup",
            "Space plants properly for good air circulation",
            "Remove any plant debris after harvest"
        ]
    },
    "Potato___Early_blight": {
        "description": "Early blight is caused by the fungus Alternaria solani. It produces dark, concentric ring lesions ('bull's-eye' pattern) on older leaves, leading to defoliation.",
        "treatment": [
            "Apply fungicides containing chlorothalonil, mancozeb, or azoxystrobin",
            "Begin sprays when disease first appears or at row closure",
            "Continue applications every 7-10 days during wet weather",
            "Remove and destroy infected plant debris after harvest",
            "Use disease forecasting models to time applications"
        ],
        "prevention": [
            "Use certified disease-free seed potatoes",
            "Rotate crops for 3-4 years away from potatoes and tomatoes",
            "Maintain plant vigor through proper fertilization",
            "Avoid overhead irrigation late in the day",
            "Destroy volunteer potatoes and nightshade weeds"
        ]
    },
    "Potato___Late_blight": {
        "description": "Late blight, caused by Phytophthora infestans, is a devastating disease that causes water-soaked lesions that turn brown and may have white fungal growth on leaf undersides.",
        "treatment": [
            "Apply fungicides containing chlorothalonil, mancozeb, or cymoxanil preventively",
            "Use systemic fungicides like propamocarb or fluopicolide for curative action",
            "Begin sprays before disease appears in wet conditions",
            "Destroy infected plants immediately to prevent spread",
            "Harvest tubers only after vines are completely dead"
        ],
        "prevention": [
            "Use certified disease-free seed potatoes",
            "Destroy cull piles and volunteer potatoes",
            "Space plants for good air circulation",
            "Avoid overhead irrigation, especially in evening",
            "Use resistant varieties when available"
        ]
    },
    "Potato___healthy": {
        "description": "Your potato plant appears healthy with no visible signs of disease or pest damage. Leaves show normal green coloration and growth.",
        "treatment": [
            "No treatment needed - continue current management",
            "Monitor for common potato pests like Colorado potato beetle",
            "Maintain consistent soil moisture during tuber development",
            "Hill soil around stems to prevent greening of tubers",
            "Apply appropriate fertilizers based on soil tests"
        ],
        "prevention": [
            "Continue regular scouting and monitoring",
            "Use certified seed potatoes",
            "Rotate crops to break pest and disease cycles",
            "Destroy volunteer potatoes and nightshade weeds",
            "Harvest tubers before soil temperatures drop too low"
        ]
    },
    "Raspberry___healthy": {
        "description": "Your raspberry plant appears healthy with no visible signs of disease or pest damage. Leaves show normal green coloration and growth.",
        "treatment": [
            "No treatment needed - continue current care",
            "Monitor for common raspberry pests and diseases",
            "Prune canes properly after fruiting",
            "Maintain adequate water during fruit development",
            "Apply mulch to retain moisture and suppress weeds"
        ],
        "prevention": [
            "Continue regular monitoring and maintenance",
            "Prune to remove spent floricanes after harvest",
            "Thin primocanes for better air circulation",
            "Remove wild brambles nearby that may harbor diseases",
            "Use drip irrigation to keep foliage dry"
        ]
    },
    "Soybean___healthy": {
        "description": "Your soybean plant appears healthy with no visible signs of disease or pest damage. Leaves show normal green coloration and growth.",
        "treatment": [
            "No treatment needed - continue current management",
            "Monitor for common soybean pests and diseases",
            "Maintain appropriate soil fertility",
            "Control weeds that compete for resources",
            "Scout regularly for early detection of issues"
        ],
        "prevention": [
            "Continue regular field scouting",
            "Use disease-resistant varieties suited to your area",
            "Rotate crops to break pest and disease cycles",
            "Use certified seed with appropriate seed treatments",
            "Manage weeds that may harbor pathogens"
        ]
    },
    "Squash___Powdery_mildew": {
        "description": "Powdery mildew is a fungal disease that appears as white, powdery spots on leaves, stems, and fruit. It thrives in warm, dry conditions with cool nights.",
        "treatment": [
            "Apply fungicides containing sulfur, myclobutanil, or potassium bicarbonate",
            "Use neem oil or horticultural oil as organic options",
            "Remove severely infected leaves to reduce inoculum",
            "Improve air circulation around plants",
            "Avoid overhead watering which can spread spores"
        ],
        "prevention": [
            "Plant resistant varieties when available",
            "Provide adequate spacing between plants",
            "Avoid excessive nitrogen fertilization",
            "Plant in full sun with good air circulation",
            "Remove plant debris after harvest"
        ]
    },
    "Strawberry___Leaf_scorch": {
        "description": "Leaf scorch is caused by the fungus Diplocarpon earlianum. It produces irregular purple to red spots that merge to form scorched appearance on leaves.",
        "treatment": [
            "Apply fungicides containing myclobutanil, captan, or thiophanate-methyl",
            "Remove and destroy infected leaves and plant debris",
            "Renovate beds after harvest to remove infected foliage",
            "Apply dormant sprays before new growth begins",
            "Improve air circulation through proper spacing"
        ],
        "prevention": [
            "Use certified disease-free plants",
            "Plant resistant varieties like 'Allstar', 'Honeoye', or 'Jewel'",
            "Remove and destroy old foliage after harvest",
            "Avoid overhead irrigation",
            "Maintain proper plant spacing for air circulation"
        ]
    },
    "Strawberry___healthy": {
        "description": "Your strawberry plant appears healthy with no visible signs of disease or pest damage. Leaves show normal green coloration and growth.",
        "treatment": [
            "No treatment needed - continue current care",
            "Monitor for common strawberry pests and diseases",
            "Maintain consistent soil moisture",
            "Renovate beds after harvest",
            "Apply mulch to keep fruit off soil"
        ],
        "prevention": [
            "Continue regular monitoring and maintenance",
            "Use certified disease-free plants",
            "Rotate beds every 3-4 years",
            "Remove runners to maintain plant vigor",
            "Use drip irrigation to keep foliage dry"
        ]
    },
    "Tomato___Bacterial_spot": {
        "description": "Bacterial spot is caused by Xanthomonas species. It produces small, water-soaked lesions on leaves that turn brown with yellow halos, and can cause significant defoliation.",
        "treatment": [
            "Apply copper-based bactericides combined with mancozeb",
            "Remove and destroy severely infected plants",
            "Avoid working in fields when foliage is wet",
            "Use fixed copper sprays at first sign of disease",
            "Apply streptomycin as a foliar spray in severe cases"
        ],
        "prevention": [
            "Use certified disease-free seed or transplants",
            "Hot-water treat seeds at 122°F for 25 minutes",
            "Avoid overhead irrigation",
            "Rotate crops for 2-3 years away from tomatoes and peppers",
            "Maintain good field sanitation"
        ]
    },
    "Tomato___Early_blight": {
        "description": "Early blight is caused by Alternaria solani. It produces dark, concentric ring lesions on older leaves, stems, and fruit, causing significant defoliation.",
        "treatment": [
            "Apply fungicides containing chlorothalonil, mancozeb, or azoxystrobin",
            "Begin sprays when first symptoms appear on lower leaves",
            "Continue applications every 7-14 days depending on weather",
            "Remove and destroy infected lower leaves",
            "Use staking and mulching to reduce contact with soil"
        ],
        "prevention": [
            "Use certified disease-free seed and transplants",
            "Rotate crops for 2-3 years away from tomatoes and potatoes",
            "Use staking and mulching to reduce soil splash",
            "Remove and destroy plant debris after harvest",
            "Maintain adequate plant nutrition"
        ]
    },
    "Tomato___Late_blight": {
        "description": "Late blight is caused by Phytophthora infestans. It produces water-soaked lesions that expand rapidly, with white fungal growth on leaf undersides. It can destroy crops within days.",
        "treatment": [
            "Apply fungicides containing chlorothalonil or mancozeb preventively",
            "Use systemic fungicides containing cymoxanil or propamocarb",
            "Begin sprays before symptoms appear in cool, wet conditions",
            "Remove and destroy infected plants immediately",
            "Harvest mature green fruit before destroying infected plants"
        ],
        "prevention": [
            "Use certified disease-free transplants",
            "Destroy volunteer tomatoes and potatoes",
            "Avoid overhead irrigation, especially in evening",
            "Space plants for good air circulation",
            "Use resistant varieties like 'Mountain Magic' or 'Defiant'"
        ]
    },
    "Tomato___Leaf_Mold": {
        "description": "Leaf mold is caused by the fungus Passalora fulva. It produces yellow spots on upper leaf surfaces with olive-green to gray mold growth on the undersides.",
        "treatment": [
            "Apply fungicides containing chlorothalonil, mancozeb, or azoxystrobin",
            "Increase greenhouse ventilation and reduce humidity",
            "Remove and destroy infected lower leaves",
            "Use resistant tomato varieties",
            "Apply sulfur-based fungicides as organic option"
        ],
        "prevention": [
            "Use resistant tomato varieties",
            "Maintain greenhouse humidity below 85%",
            "Provide adequate plant spacing for air circulation",
            "Avoid overhead watering in greenhouses",
            "Remove and destroy plant debris after harvest"
        ]
    },
    "Tomato___Septoria_leaf_spot": {
        "description": "Septoria leaf spot is caused by the fungus Septoria lycopersici. It produces circular spots with dark borders and gray centers on leaves, starting from lower leaves.",
        "treatment": [
            "Apply fungicides containing chlorothalonil, mancozeb, or copper",
            "Begin sprays when first symptoms appear",
            "Remove and destroy infected lower leaves",
            "Apply mulch around base of plants to reduce soil splash",
            "Use staking to keep foliage off the ground"
        ],
        "prevention": [
            "Remove and destroy plant debris after harvest",
            "Rotate crops for 2-3 years away from tomatoes",
            "Use drip irrigation to keep foliage dry",
            "Provide adequate spacing for air circulation",
            "Use mulch to prevent soil splash onto leaves"
        ]
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "description": "Two-spotted spider mites are tiny arachnids that cause yellow stippling on leaves, progressing to bronzing and leaf drop. Fine webbing may be visible on plants.",
        "treatment": [
            "Apply miticides containing abamectin, bifenazate, or spiromesifen",
            "Use insecticidal soap or horticultural oil for light infestations",
            "Release predatory mites like Phytoseiulus persimilis for biological control",
            "Remove heavily infested leaves or plants",
            "Avoid broad-spectrum insecticides that kill natural enemies"
        ],
        "prevention": [
            "Maintain adequate plant hydration",
            "Avoid dusty conditions around plants",
            "Conserve natural enemies like predatory mites and insects",
            "Monitor regularly for early detection using a hand lens",
            "Remove weeds that can harbor mite populations"
        ]
    },
    "Tomato___Target_Spot": {
        "description": "Target spot is caused by the fungus Corynespora cassiicola. It produces circular lesions with concentric rings resembling a target, starting on lower leaves.",
        "treatment": [
            "Apply fungicides containing chlorothalonil, mancozeb, or azoxystrobin",
            "Remove and destroy infected lower leaves",
            "Improve air circulation through proper pruning",
            "Avoid overhead irrigation to reduce leaf wetness",
            "Apply preventive fungicide sprays during humid conditions"
        ],
        "prevention": [
            "Remove and destroy plant debris after harvest",
            "Use drip irrigation to keep foliage dry",
            "Provide adequate plant spacing for air circulation",
            "Avoid excessive nitrogen fertilization",
            "Rotate crops to reduce pathogen buildup"
        ]
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "description": "TYLCV is a devastating viral disease transmitted by whiteflies. It causes yellowing, curling of leaves, stunting, and significant yield loss.",
        "treatment": [
            "No cure exists for viral diseases - prevention is essential",
            "Remove and destroy infected plants immediately",
            "Control whitefly vectors with insecticides",
            "Use reflective mulches to repel whiteflies",
            "Apply insecticidal soaps or oils for whitefly control"
        ],
        "prevention": [
            "Use TYLCV-resistant varieties like 'Tygress', 'Security', or 'SV8546TE'",
            "Control whiteflies with regular insecticide applications",
            "Use virus-free transplants from certified sources",
            "Install reflective mulches to repel whiteflies",
            "Remove weeds and volunteer tomatoes that harbor whiteflies"
        ]
    },
    "Tomato___Tomato_mosaic_virus": {
        "description": "Tomato mosaic virus causes mottled light and dark green patterns on leaves, leaf curling, and stunting. It can also cause fruit deformities.",
        "treatment": [
            "No cure exists for viral diseases - prevention is key",
            "Remove and destroy infected plants immediately",
            "Disinfect tools and hands after handling infected plants",
            "Control aphids and other vectors",
            "Avoid smoking near tomatoes as tobacco carries related viruses"
        ],
        "prevention": [
            "Use virus-resistant varieties when available",
            "Use virus-free certified seed",
            "Disinfect tools and wash hands between plants",
            "Control aphids and other potential vectors",
            "Avoid smoking near tomato plants"
        ]
    },
    "Tomato___healthy": {
        "description": "Your tomato plant appears healthy with no visible signs of disease or pest damage. Leaves show normal green coloration and growth pattern.",
        "treatment": [
            "No treatment needed - continue current care",
            "Monitor for common tomato pests and diseases",
            "Maintain consistent soil moisture",
            "Prune suckers for better air circulation",
            "Provide support with cages or stakes"
        ],
        "prevention": [
            "Continue regular monitoring and maintenance",
            "Use mulch to retain moisture and prevent soil splash",
            "Rotate crops annually to prevent disease buildup",
            "Space plants properly for good air circulation",
            "Remove plant debris after harvest"
        ]
    }
}


def get_disease_info(disease_name: str) -> dict:
    """
    Get treatment and prevention information for a disease.
    
    Args:
        disease_name: Name of the disease class
        
    Returns:
        Dictionary with description, treatment, and prevention
    """
    return TREATMENT_DATA.get(disease_name, {
        "description": f"Information about {disease_name}",
        "treatment": ["Consult a plant pathologist for specific treatment recommendations"],
        "prevention": ["Practice good sanitation and crop management"]
    })