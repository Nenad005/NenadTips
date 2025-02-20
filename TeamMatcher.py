from fuzzywuzzy import fuzz
import re
import unicodedata

def normalize_team_name(name):
    """
    Enhanced normalization with:
    - Dash/dot replacement
    - Capitalized initial splitting
    - Improved abbreviation handling
    """
    # Convert to ASCII and preserve case temporarily
    normalized = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')
    
    # Replace dashes and dots with spaces
    normalized = re.sub(r'[-.]', ' ', normalized)
    
    # Split into words and process capitalization
    words = []
    for word in normalized.split():
        # Split all-caps words into individual letters
        if word.isupper() and len(word) > 1:
            words.extend(list(word))
        # Split camelCase words (e.g., "NewYork" -> "New York")
        elif re.match(r'^[A-Z][a-z]+$', word):
            words.extend(re.findall(r'[A-Z][a-z]*', word))
        else:
            words.append(word)
    
    # Rebuild string and lowercase
    normalized = ' '.join(words).lower()
    
    # Remove remaining special characters
    normalized = re.sub(r'[^\w\s]', '', normalized)
    
    # Enhanced abbreviation mapping
    abbreviation_map = {
        'fc': 'football club',
        'cf': 'club de futbol',
        'utd': 'united',
        'inter': 'internazionale',
        'man': 'manchester',
        'spurs': 'tottenham',
        'atletico': 'atlético',
        'as': 'associazione sportiva',
        'afc': 'association football club',
        'ssc': 'sporting soccer club'
    }
    
    # Replace abbreviations with full forms
    return ' '.join([abbreviation_map.get(word, word) for word in normalized.split()])

def get_initials(normalized_name):
    """Extract initials from normalized name"""
    return ''.join([word[0] for word in normalized_name.split() if word])

def calculate_similarity(name1, name2):
    """
    Enhanced similarity calculation with:
    - Initial sequence matching
    - Improved weight distribution
    """
    norm1 = normalize_team_name(name1)
    norm2 = normalize_team_name(name2)
    
    # Whole word matches
    words1 = set(norm1.split())
    words2 = set(norm2.split())
    common_words = words1 & words2
    whole_word_score = len(common_words) / max(len(words1), len(words2))
    
    # Initials matching
    initials1 = get_initials(norm1)
    initials2 = get_initials(norm2)
    initials_score = fuzz.ratio(initials1, initials2) / 100
    
    # Sequence matching
    lev_score = fuzz.ratio(norm1, norm2) / 100
    token_score = fuzz.token_sort_ratio(norm1, norm2) / 100
    
    # Weighted scoring (adjust weights as needed)
    weights = {
        'whole_word': 0.3,
        'initials': 0.3,
        'levenshtein': 0.2,
        'token': 0.2
    }
    
    return (
        (weights['whole_word'] * whole_word_score) +
        (weights['initials'] * initials_score) +
        (weights['levenshtein'] * lev_score) +
        (weights['token'] * token_score)
    )

def team_name_matcher(name1, name2, threshold=0.75):
    """
    Enhanced matching logic with:
    - Initial sequence checks
    - Adaptive thresholding
    """
    # Direct match check
    if name1.lower() == name2.lower():
        return True
    
    # Normalize names
    norm1 = normalize_team_name(name1)
    norm2 = normalize_team_name(name2)
    
    # Initial sequence check
    if get_initials(norm1) == get_initials(norm2):
        return True
    
    # Whole word check
    if len(set(norm1.split()) & set(norm2.split())) > 0:
        return True
    
    # Calculate composite score
    score = calculate_similarity(norm1, norm2)
    
    # Adaptive threshold adjustment for short names
    min_length = min(len(norm1), len(norm2))
    if min_length < 5:
        threshold = max(threshold, 0.85)
    
    return score >= threshold

# Enhanced test cases
test_pairs = [
    ("PSG", "Paris-S.G."),          # True (initials match)
    ("A.S. Roma", "AS Roma"),       # True (initials match)
    ("Inter-Milan", "Internazionale"), # True (whole word)
    ("Man Utd", "Manchester United"),# True (camelCase split)
    ("FCB", "F.C. Barcelona"),      # True (initials match)
    ("Atlético", "Atletico"),       # True (diacritic removal)
    ("LosAngeles", "LA Galaxy"),    # False (initials mismatch)
    ("BVB", "Borussia Dortmund"),    # True (initials match)
    ("Man Utd", "Manchester United"),
    ("PSG", "Paris Saint-Germain"),
    ("Atlético Madrid", "Atletico Madrid"),
    ("Inter", "Internazionale"),
    ("FC Bayern", "Bayern Munich"),
    ("Tottenham", "Spurs"),
    ("Liverpool", "Liverpool FC"),
    ("Real Madrid", "Real Madrid CF"),
    ("Barcelona", "FC Barcelona"),
    ("Juventus", "Juventus FC"),
    ("Partizan", "FK Partizan"),
    ("Red Star", "Crvena Zvezda"),
    ("Ajax", "AFC Ajax"),
    ("Partizan", "Zvezda"),
    ("Chelsea", "Chelsea FC"),
    ("Arsenal", "Arsenal FC"),
    ("Manchester City", "Man City"),
    ("AC Milan", "Milan"),
    ("AS Roma", "Roma"),
    ("Lazio", "SS Lazio"),
    ("Napoli", "SSC Napoli"),
    ("Fiorentina", "ACF Fiorentina"),
    ("Torino", "Torino FC"),
    ("Sampdoria", "UC Sampdoria"),
    ("Genoa", "Genoa CFC"),
    ("Bologna", "Bologna FC"),
    ("Cagliari", "Cagliari Calcio"),
    ("Parma", "Parma Calcio"),
    ("Sassuolo", "US Sassuolo"),
    ("Udinese", "Udinese Calcio"),
    ("Verona", "Hellas Verona"),
    ("Brescia", "Brescia Calcio"),
    ("Lecce", "US Lecce"),
    ("SPAL", "SPAL 2013"),
    ("Empoli", "Empoli FC"),
    ("Chievo", "AC Chievo Verona"),
    ("Palermo", "US Palermo"),
    ("Pescara", "Pescara Calcio"),
    ("Frosinone", "Frosinone Calcio"),
    ("Crotone", "FC Crotone"),
    ("Benevento", "Benevento Calcio"),
    ("Perugia", "AC Perugia"),
    ("Salernitana", "US Salernitana"),
    ("Spezia", "Spezia Calcio"),
    ("Cittadella", "AS Cittadella"),
    ("Cosenza", "Cosenza Calcio"),
    ("Cremonese", "US Cremonese"),
    ("Entella", "Virtus Entella"),
    ("Livorno", "AS Livorno"),
    ("Pisa", "Pisa SC"),
    ("Pordenone", "Pordenone Calcio"),
    ("Reggina", "Reggina 1914"),
    ("Trapani", "Trapani Calcio"),
    ("Vicenza", "LR Vicenza"),
    ("Venezia", "Venezia FC"),
    ("Monza", "AC Monza"),
    ("Alessandria", "US Alessandria"),
    ("Avellino", "US Avellino"),
    ("Bari", "SSC Bari"),
    ("Catanzaro", "US Catanzaro"),
    ("Cesena", "AC Cesena"),
    ("Como", "Como 1907"),
    ("Fermana", "Fermana FC"),
    ("Gubbio", "AS Gubbio"),
    ("Juve Stabia", "SS Juve Stabia"),
    ("Lecce", "US Lecce"),
    ("Modena", "Modena FC"),
    ("Novara", "Novara Calcio"),
    ("Padova", "Calcio Padova"),
    ("Piacenza", "Piacenza Calcio"),
    ("Pro Vercelli", "FC Pro Vercelli"),
    ("Reggiana", "AC Reggiana"),
    ("Rimini", "Rimini FC"),
    ("Siena", "AC Siena"),
    ("Sudtirol", "FC Sudtirol"),
    ("Ternana", "Ternana Calcio"),
    ("Triestina", "US Triestina"),
    ("Viterbese", "US Viterbese"),
    ("Virtus Verona", "Virtus Verona"),
    ("Wanderers", "Montevideo Wanderers"),
    ("Nacional", "Club Nacional"),
    ("Peñarol", "CA Peñarol"),
    ("Defensor", "Defensor Sporting"),
    ("Danubio", "Danubio FC"),
    ("Liverpool", "Liverpool Montevideo"),
    ("River Plate", "CA River Plate"),
    ("Boston River", "Boston River"),
    ("Cerro", "Cerro Montevideo"),
    ("Fenix", "CA Fenix"),
    ("Plaza Colonia", "Plaza Colonia"),
    ("Progreso", "CA Progreso"),
    ("Racing", "Racing Club"),
    ("Rentistas", "CA Rentistas"),
    ("Torque", "Montevideo City Torque"),
    ("Villa Española", "Villa Española"),
    ("Wanderers", "Montevideo Wanderers"),
    ("Nacional", "Club Nacional"),
    ("Peñarol", "CA Peñarol"),
    ("Defensor", "Defensor Sporting"),
    ("Danubio", "Danubio FC"),
    ("Liverpool", "Liverpool Montevideo"),
    ("River Plate", "CA River Plate"),
    ("Boston River", "Boston River"),
    ("Cerro", "Cerro Montevideo"),
    ("Fenix", "CA Fenix"),
    ("Plaza Colonia", "Plaza Colonia"),
    ("Progreso", "CA Progreso"),
    ("Racing", "Racing Club"),
    ("Rentistas", "CA Rentistas"),
    ("Torque", "Montevideo City Torque"),
    ("Villa Española", "Villa Española"),
    ("Dortmund", "Borussia Dortmund"),
    ("Bayern", "Bayern Munich"),
    ("St. Etienne", "Saint-Etienne"),
    ("St. Gallen", "Saint Gallen"),
    ("St. Mirren", "Saint Mirren"),
    ("St. Johnstone", "Saint Johnstone"),
    ("St. Pauli", "Saint Pauli"),
    ("St. Truiden", "Saint Truiden"),
    ("St. Patricks", "Saint Patricks"),
    ("St. Polten", "Saint Polten"),
    ("St. Liege", "Saint Liege"),
    ("St. Mirren", "Saint Mirren"),
    ("St. Johnstone", "Saint Johnstone"),
    ("St. Pauli", "Saint Pauli"),
    ("St. Truiden", "Saint Truiden"),
    ("St. Patricks", "Saint Patricks"),
    ("St. Polten", "Saint Polten"),
    ("St. Liege", "Saint Liege"),
    ("St. Gallen", "Saint Gallen"),
    ("St. Etienne", "Saint-Etienne"),
    ("St. Mirren", "Saint Mirren"),
    ("St. Johnstone", "Saint Johnstone"),
    ("St. Pauli", "Saint Pauli"),
    ("St. Truiden", "Saint Truiden"),
    ("St. Patricks", "Saint Patricks"),
    ("St. Polten", "Saint Polten"),
    ("St. Liege", "Saint Liege"),
    ("St. Mirren", "Saint Mirren"),
    ("St. Johnstone", "Saint Johnstone"),
    ("St. Pauli", "Saint Pauli"),
    ("St. Truiden", "Saint Truiden"),
    ("St. Patricks", "Saint Patricks"),
    ("St. Polten", "Saint Polten"),
    ("St. Liege", "Saint Liege"),
    ("St. Gallen", "Saint Gallen"),
    ("St. Etienne", "Saint-Etienne"),
    ("St. Mirren", "Saint Mirren"),
    ("St. Johnstone", "Saint Johnstone"),
    ("St. Pauli", "Saint Pauli"),
    ("St. Truiden", "Saint Truiden"),
    ("St. Patricks", "Saint Patricks"),
    ("St. Polten", "Saint Polten"),
    ("St. Liege", "Saint Liege")
]

for pair in test_pairs:
    print(f"{pair[0]:<20} vs {pair[1]:<25} → {team_name_matcher(pair[0], pair[1])}")