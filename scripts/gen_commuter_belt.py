#!/usr/bin/env python3
"""
Generate 30 commuter-belt hub pages + 1 master index under /areas/commuter/.

Each page targets "Architectural Drawings in {Town}" and related long-tails
such as "planning permission {town}", positioning Architectural Drawings
London as a MCIAT-chartered practice covering the M25 commuter belt from
our London base (within our 50-mile service radius).

Usage:
    cd architectural-drawings
    python scripts/gen_commuter_belt.py
"""

import sys
import os
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSS_PATH = PROJECT_ROOT / "assets" / "css" / "style.css"
OUT_DIR = PROJECT_ROOT / "areas" / "commuter"

# Make sibling scripts importable (not strictly required here but kept for
# consistency with other generators)
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

# ---------------------------------------------------------------------------
# Read external CSS for inlining
# ---------------------------------------------------------------------------
css_source = CSS_PATH.read_text(encoding="utf-8")

# Strip the @import for Google Fonts (loaded via <link> tags instead)
css_inline = css_source.replace(
    "@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,200..900,0..100;1,9..144,200..900,0..100&family=Manrope:wght@300;400;500;600;700;800&display=swap');",
    "/* Fonts loaded via non-blocking link tags in the document head */"
)


def minify_css(css: str) -> str:
    """Very light CSS minification (comments + collapse whitespace)."""
    import re
    # Strip /* ... */ comments
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)
    # Collapse whitespace
    css = re.sub(r"\s+", " ", css)
    # Tighten around punctuation
    css = re.sub(r"\s*([{};:,>])\s*", r"\1", css)
    # Remove trailing semicolon before }
    css = css.replace(";}", "}")
    return css.strip()


css_min = minify_css(css_inline)
# Escape braces for f-string usage
css_escaped = css_min.replace("{", "{{").replace("}", "}}")


# ---------------------------------------------------------------------------
# Commuter-belt town data (30 towns, prioritised by search volume + distance)
# ---------------------------------------------------------------------------
TOWNS = {
    # ----- Surrey (7) -----
    "guildford": {
        "name": "Guildford",
        "county": "Surrey",
        "council": "Guildford Borough Council",
        "postcodes": "GU1, GU2, GU3, GU4",
        "distance_from_london": "28 miles",
        "travel_time": "35 min from London Waterloo",
        "typical_housing": "Victorian/Edwardian terraces in town centre, 1930s semis, rural cottages in surrounding villages, and modern estates towards Merrow and Burpham.",
        "conservation_notes": "Guildford town centre, Merrow, Shalford and Chilworth are designated conservation areas with strict design controls on materials, fenestration and extensions.",
        "character": "Affluent cathedral and university town with a historic cobbled High Street, ranked among the UK's most prosperous commuter hubs.",
        "nearby_towns": ["woking", "dorking", "leatherhead"],
        "planning_quirks": "Guildford's Local Plan (2019) favours dense redevelopment of brownfield sites while protecting the rural setting. Metropolitan Green Belt covers roughly 89% of the borough, so extensions outside the urban envelope face strict openness tests.",
    },
    "woking": {
        "name": "Woking",
        "county": "Surrey",
        "council": "Woking Borough Council",
        "postcodes": "GU21, GU22, GU24",
        "distance_from_london": "23 miles",
        "travel_time": "26 min from London Waterloo",
        "typical_housing": "Mix of Edwardian villas in Horsell, 1930s semis across Maybury and Sheerwater, plus new apartment towers around the regenerated town centre.",
        "conservation_notes": "Horsell Village, Old Woking and Brookwood Cemetery are conservation areas. The Brookwood Necropolis is Grade I registered.",
        "character": "Rapidly densifying town with Sir Norman Foster's Lightbox and extensive new high-rise residential, while rural parishes retain Green Belt character.",
        "nearby_towns": ["guildford", "staines-upon-thames", "leatherhead"],
        "planning_quirks": "Woking's adopted Core Strategy directs most growth to the town centre. Outside the urban area, the Green Belt and Thames Basin Heaths SPA (400m buffer) significantly restrict new residential development.",
    },
    "epsom": {
        "name": "Epsom",
        "county": "Surrey",
        "council": "Epsom and Ewell Borough Council",
        "postcodes": "KT17, KT18, KT19",
        "distance_from_london": "15 miles",
        "travel_time": "35 min from London Waterloo",
        "typical_housing": "1930s mock-Tudor semis dominate Stoneleigh and Ewell, with Georgian and Regency townhouses around the High Street and interwar suburbs throughout.",
        "conservation_notes": "Epsom Town Centre, Church Street, Woodcote and Stamford Green are conservation areas. The Epsom Downs racecourse is a Grade II registered landscape.",
        "character": "Quintessential Surrey commuter town synonymous with Derby Day; strong architectural variety from Georgian to late-20th-century.",
        "nearby_towns": ["leatherhead", "dorking", "reigate"],
        "planning_quirks": "Epsom and Ewell has the smallest area of any Surrey district and is almost fully built-out. The Local Plan prioritises intensification over Green Belt release, so most new schemes are extensions, infill and subdivisions.",
    },
    "reigate": {
        "name": "Reigate",
        "county": "Surrey",
        "council": "Reigate and Banstead Borough Council",
        "postcodes": "RH1, RH2",
        "distance_from_london": "21 miles",
        "travel_time": "40 min from London Bridge",
        "typical_housing": "Period cottages in the old town, interwar semis, and substantial detached houses on the wooded slopes of Reigate Hill and Reigate Heath.",
        "conservation_notes": "Reigate Town, Reigate Heath, Park Lane and Reigate Hill are conservation areas. Parts of the borough lie within the Surrey Hills AONB.",
        "character": "Historic market town at the foot of the North Downs, combining a medieval street pattern with affluent commuter suburbia.",
        "nearby_towns": ["dorking", "epsom", "sevenoaks"],
        "planning_quirks": "The Surrey Hills Area of Outstanding Natural Beauty covers much of the southern borough, and the Green Belt ring tightly constrains expansion. Reigate Castle grounds are a Scheduled Monument.",
    },
    "dorking": {
        "name": "Dorking",
        "county": "Surrey",
        "council": "Mole Valley District Council",
        "postcodes": "RH4, RH5",
        "distance_from_london": "25 miles",
        "travel_time": "50 min from London Waterloo",
        "typical_housing": "Georgian and Victorian townhouses in the town centre, Arts and Crafts villas on the outskirts, and rural farmhouses and cottages in the surrounding Surrey Hills villages.",
        "conservation_notes": "Dorking Town Centre, Westcott, Brockham and Mickleham are conservation areas. Box Hill and Denbies Hillside are Sites of Special Scientific Interest within the AONB.",
        "character": "Picturesque market town at the foot of Box Hill, sitting entirely within the Surrey Hills AONB.",
        "nearby_towns": ["reigate", "leatherhead", "guildford"],
        "planning_quirks": "The Surrey Hills AONB status means any application must demonstrate that landscape impact is minimised. Mole Valley's Green Belt review is ongoing and remains restrictive on new dwellings outside defined settlements.",
    },
    "staines-upon-thames": {
        "name": "Staines-upon-Thames",
        "county": "Surrey",
        "council": "Spelthorne Borough Council",
        "postcodes": "TW18, TW19",
        "distance_from_london": "19 miles",
        "travel_time": "35 min from London Waterloo",
        "typical_housing": "Postwar semis and terraces, 1960s-80s estates, Thames-side cottages along Church Lammas, and contemporary apartment blocks near the station and riverside.",
        "conservation_notes": "Staines Town Centre and Laleham Village are conservation areas. Large parts of the borough sit within Flood Zones 2 and 3 from the Thames and its tributaries.",
        "character": "Thames-side town on the edge of the M25, dominated by the river, reservoirs and proximity to Heathrow.",
        "nearby_towns": ["woking", "windsor", "slough"],
        "planning_quirks": "Spelthorne sits within the 6.5km Heathrow Public Safety Zone in places, and flood-risk sequential testing applies to much of the riverside plot stock. Green Belt covers about 60% of the borough.",
    },
    "leatherhead": {
        "name": "Leatherhead",
        "county": "Surrey",
        "council": "Mole Valley District Council",
        "postcodes": "KT22, KT23, KT24",
        "distance_from_london": "20 miles",
        "travel_time": "40 min from London Waterloo",
        "typical_housing": "Tudor and Georgian cottages in the old town, Edwardian villas around the commons, 1930s semis along the A24 corridor, and executive estates in Fetcham and Bookham.",
        "conservation_notes": "Leatherhead Town, Fetcham, Great Bookham and Ashtead Village are conservation areas; the River Mole corridor is environmentally sensitive.",
        "character": "Commuter town straddling the River Mole at the gateway to the Surrey Hills AONB.",
        "nearby_towns": ["dorking", "epsom", "guildford"],
        "planning_quirks": "Much of Leatherhead's rural hinterland is designated Green Belt within the Surrey Hills AONB, which places a very high landscape bar on any visible extensions or new builds outside the settlement boundaries.",
    },
    # ----- Hertfordshire (6) -----
    "watford": {
        "name": "Watford",
        "county": "Hertfordshire",
        "council": "Watford Borough Council",
        "postcodes": "WD17, WD18, WD19, WD24, WD25",
        "distance_from_london": "17 miles",
        "travel_time": "20 min from London Euston",
        "typical_housing": "Dense Victorian/Edwardian terraces in Cassiobury and Nascot, interwar semis across Oxhey and North Watford, and significant postwar council estates plus modern tall apartment blocks in the town centre.",
        "conservation_notes": "Nascot, Cassiobury and Watford Heath are conservation areas. Cassiobury Park is a Grade II registered landscape.",
        "character": "The largest town in Hertfordshire: major retail, media (including Warner Bros Studios Leavesden) and densifying high-rise residential.",
        "nearby_towns": ["hemel-hempstead", "st-albans", "stevenage"],
        "planning_quirks": "Watford is compact and almost fully built-out; the Local Plan 2020-38 favours tall buildings in the town centre. Much of the borough is outside the Green Belt, but householder PD rights are restricted in several Article 4 conservation areas.",
    },
    "st-albans": {
        "name": "St Albans",
        "county": "Hertfordshire",
        "council": "St Albans City and District Council",
        "postcodes": "AL1, AL3, AL4",
        "distance_from_london": "22 miles",
        "travel_time": "19 min from London St Pancras",
        "typical_housing": "Medieval and Georgian townhouses around the cathedral, Victorian terraces in Fleetville, interwar semis across Marshalswick, and rural cottages in the surrounding Chiltern villages.",
        "conservation_notes": "St Albans has 16 conservation areas including the Cathedral, Romeland, Sopwell and Fishpool Street. The Roman city of Verulamium is a Scheduled Monument directly abutting modern development.",
        "character": "Historic cathedral city with Roman foundations; consistently ranked among the most desirable commuter destinations.",
        "nearby_towns": ["watford", "hemel-hempstead", "hertford"],
        "planning_quirks": "St Albans has an Article 4 Direction covering HMO conversions across parts of the city. The district is 81% Green Belt, and many streets have additional Article 4 removing PD rights on terraced frontages.",
    },
    "hemel-hempstead": {
        "name": "Hemel Hempstead",
        "county": "Hertfordshire",
        "council": "Dacorum Borough Council",
        "postcodes": "HP1, HP2, HP3",
        "distance_from_london": "27 miles",
        "travel_time": "30 min from London Euston",
        "typical_housing": "Original Old Town Georgian cottages, extensive 1950s-60s New Town estates (Adeyfield, Highfield, Grovehill), and modern cul-de-sac developments at Gadebridge and Leverstock Green.",
        "conservation_notes": "Hemel Hempstead Old Town is a tightly-controlled conservation area. The Gade Valley through the town is a designated wildlife corridor.",
        "character": "Post-war New Town designed around a neighbourhood unit model, anchored by the distinctive Magic Roundabout and modernist Civic Centre.",
        "nearby_towns": ["watford", "st-albans", "amersham"],
        "planning_quirks": "Dacorum retains strong Green Belt designations over the Chilterns and Ashridge Estate. The New Town's Radburn-style layouts mean many houses have unusual plot geometries that require careful rear-extension design.",
    },
    "hertford": {
        "name": "Hertford",
        "county": "Hertfordshire",
        "council": "East Hertfordshire District Council",
        "postcodes": "SG13, SG14",
        "distance_from_london": "22 miles",
        "travel_time": "45 min from London Liverpool Street",
        "typical_housing": "Timber-framed medieval cottages in the old town, Georgian and Victorian townhouses along Fore Street, Edwardian villas in Bengeo, and 20th-century estates at Sele Farm and Chelmsford Road.",
        "conservation_notes": "Hertford Town, Bengeo, Port Hill and Hertingfordbury are conservation areas. Hertford Castle is a Scheduled Monument.",
        "character": "County town of Hertfordshire at the confluence of four rivers, rich in listed buildings and medieval street patterns.",
        "nearby_towns": ["welwyn-garden-city", "stevenage", "harlow"],
        "planning_quirks": "East Herts Local Plan 2018 protects the Green Belt between Hertford and the M25 tightly. The Lea Valley Regional Park designation covers the eastern edge and imposes additional landscape controls.",
    },
    "stevenage": {
        "name": "Stevenage",
        "county": "Hertfordshire",
        "council": "Stevenage Borough Council",
        "postcodes": "SG1, SG2",
        "distance_from_london": "30 miles",
        "travel_time": "22 min from London King's Cross",
        "typical_housing": "Britain's first designated New Town: Radburn-layout 1950s-60s estates (Bedwell, Shephall, Chells), plus some surviving Old Town Georgian houses and a wave of modern apartments around the station.",
        "conservation_notes": "Stevenage Old Town High Street is the principal conservation area. Knebworth Park lies just outside the borough.",
        "character": "Post-war New Town with Britain's first pedestrianised town centre, now the subject of a major town-centre regeneration programme.",
        "nearby_towns": ["welwyn-garden-city", "st-albans", "hertford"],
        "planning_quirks": "Stevenage's Local Plan 2019 supports intensification, but its tight urban boundary means Green Belt release is carefully sequenced. Many New Town houses were built to Parker-Morris standards and have low floor-to-ceiling heights affecting loft conversion viability.",
    },
    "welwyn-garden-city": {
        "name": "Welwyn Garden City",
        "county": "Hertfordshire",
        "council": "Welwyn Hatfield Borough Council",
        "postcodes": "AL7, AL8",
        "distance_from_london": "21 miles",
        "travel_time": "25 min from London King's Cross",
        "typical_housing": "Garden City semis and terraces to Ebenezer Howard's 1920 plan (neo-Georgian with generous gardens), Louis de Soissons civic buildings, and postwar extensions to the north and east.",
        "conservation_notes": "Almost the entirety of the original Garden City is a conservation area with a detailed Design Code. Sherrardspark Wood is an SSSI directly abutting housing.",
        "character": "The second Garden City in Britain and a protected exemplar of early 20th-century town planning.",
        "nearby_towns": ["hertford", "stevenage", "st-albans"],
        "planning_quirks": "The Welwyn Garden City Conservation Area Appraisal restricts front-elevation alterations, window changes, and any materials other than the original neo-Georgian palette. Article 4 Directions add further controls on roof alterations, porches and boundary treatments.",
    },
    # ----- Essex (5) -----
    "brentwood": {
        "name": "Brentwood",
        "county": "Essex",
        "council": "Brentwood Borough Council",
        "postcodes": "CM13, CM14, CM15",
        "distance_from_london": "20 miles",
        "travel_time": "35 min from London Liverpool Street (Elizabeth line)",
        "typical_housing": "Victorian cottages in Brentwood High Street, 1930s semis across Warley and Hutton, and substantial executive detached homes in Shenfield, Ingatestone and the rural wards.",
        "conservation_notes": "Brentwood Town Centre, Great Warley, Ingatestone and Blackmore are conservation areas. The Thorndon Park Registered Landscape is Grade II.",
        "character": "Affluent commuter town directly served by Elizabeth line since 2022, raising property values and densification pressure.",
        "nearby_towns": ["chelmsford", "epping", "loughton"],
        "planning_quirks": "Brentwood is 89% Green Belt, so almost all growth must be either on previously-developed land or through the Local Plan's managed Green Belt release sites. Article 4 Directions apply at Thorndon Park and parts of Warley.",
    },
    "chelmsford": {
        "name": "Chelmsford",
        "county": "Essex",
        "council": "Chelmsford City Council",
        "postcodes": "CM1, CM2, CM3",
        "distance_from_london": "32 miles",
        "travel_time": "35 min from London Liverpool Street",
        "typical_housing": "Georgian townhouses around the cathedral, Victorian and Edwardian terraces in Moulsham and Springfield, extensive interwar and postwar suburbs, and the large modern Beaulieu Park development to the north-east.",
        "conservation_notes": "Chelmsford Central, Moulsham Street, Springfield and Great Baddow are conservation areas. The cathedral precinct is Grade I listed.",
        "character": "County town and cathedral city; one of England's fastest-growing cities with major town-centre regeneration.",
        "nearby_towns": ["brentwood", "harlow", "epping"],
        "planning_quirks": "Chelmsford's Local Plan (adopted 2020) allocates a significant new garden community north of Boreham. Flood risk from the Chelmer and Can constrains riverside plots, and the 400m buffer around Essex Coast Recreational Areas of Protection (RAMS) applies across the city.",
    },
    "harlow": {
        "name": "Harlow",
        "county": "Essex",
        "council": "Harlow District Council",
        "postcodes": "CM17, CM18, CM19, CM20",
        "distance_from_london": "25 miles",
        "travel_time": "35 min from London Liverpool Street",
        "typical_housing": "Sir Frederick Gibberd's 1947 New Town master plan: neighbourhood-based 1950s-60s estates with distinctive modernist details, plus some surviving Old Harlow period buildings and modern infill.",
        "conservation_notes": "Old Harlow, Churchgate Street and Harlow Common are conservation areas. The Gibberd Garden is Grade II registered.",
        "character": "Britain's third major post-war New Town, designed as a set of self-contained neighbourhoods around a central pedestrian precinct.",
        "nearby_towns": ["epping", "hertford", "chelmsford"],
        "planning_quirks": "Harlow sits at the centre of the Harlow and Gilston Garden Town, an ambitious cross-boundary growth area. Many New Town streets are under Article 4 to preserve the original Gibberd design vocabulary, restricting porch additions, window changes and front-elevation extensions.",
    },
    "epping": {
        "name": "Epping",
        "county": "Essex",
        "council": "Epping Forest District Council",
        "postcodes": "CM16",
        "distance_from_london": "17 miles",
        "travel_time": "30 min via Central line",
        "typical_housing": "Georgian and Victorian cottages along Epping High Street, Edwardian villas, 1930s semis, and executive modern homes on the fringes of the Forest.",
        "conservation_notes": "Epping Town, Theydon Bois and North Weald Bassett are conservation areas. Epping Forest itself is a Site of Special Scientific Interest and Special Area of Conservation.",
        "character": "Historic market town, Central line terminus, gateway to Epping Forest.",
        "nearby_towns": ["loughton", "harlow", "brentwood"],
        "planning_quirks": "The Epping Forest SAC requires a 6.2km zone of influence with additional mitigation for any new residential development that increases visitor pressure. 92% of the district is Green Belt.",
    },
    "loughton": {
        "name": "Loughton",
        "county": "Essex",
        "council": "Epping Forest District Council",
        "postcodes": "IG10",
        "distance_from_london": "13 miles",
        "travel_time": "30 min via Central line",
        "typical_housing": "Edwardian and 1930s semis across High Beach, Goldings Hill and Loughton Broadway, period cottages in the High Road conservation area, and substantial detached homes on the Forest edge.",
        "conservation_notes": "Loughton High Road, Goldings Hill and Loughton Park are conservation areas. The adjacent Epping Forest is an SAC with strict landscape controls.",
        "character": "Affluent Essex commuter town on the Central line, with many homes backing directly onto Epping Forest.",
        "nearby_towns": ["epping", "brentwood", "harlow"],
        "planning_quirks": "The Epping Forest SAC 6.2km zone of influence applies to almost the entire urban area of Loughton. New dwellings or additional bedrooms may require mitigation contributions via the Local Plan's SAMM/SANGS system.",
    },
    # ----- Kent (5) -----
    "sevenoaks": {
        "name": "Sevenoaks",
        "county": "Kent",
        "council": "Sevenoaks District Council",
        "postcodes": "TN13, TN14, TN15",
        "distance_from_london": "22 miles",
        "travel_time": "28 min from London Charing Cross",
        "typical_housing": "Georgian and Regency townhouses along the High Street, Victorian villas in St Johns, Edwardian and interwar semis, and substantial detached homes on the Kent Downs.",
        "conservation_notes": "Sevenoaks Town, Riverhead, Kippington and Seal are conservation areas. The Kent Downs AONB covers the majority of the district.",
        "character": "Historic town beside Knole Park, one of the most expensive property markets outside London.",
        "nearby_towns": ["tunbridge-wells", "tonbridge", "dartford"],
        "planning_quirks": "Sevenoaks district is 93% Green Belt and 60% Kent Downs AONB, a combination that makes almost all rural development extremely difficult. Knole Park is a Grade I registered landscape and a Scheduled Monument.",
    },
    "tunbridge-wells": {
        "name": "Tunbridge Wells",
        "county": "Kent",
        "council": "Tunbridge Wells Borough Council",
        "postcodes": "TN1, TN2, TN3, TN4",
        "distance_from_london": "33 miles",
        "travel_time": "48 min from London Charing Cross",
        "typical_housing": "Regency and early Victorian townhouses around the Pantiles and Mount Ephraim, Decimus Burton villas, Edwardian terraces, and Arts and Crafts homes in Rusthall and Langton Green.",
        "conservation_notes": "Tunbridge Wells has 14 conservation areas, including Royal Tunbridge Wells Central, Mount Sion and the Pantiles. Many homes are within the High Weald AONB.",
        "character": "Regency spa town granted its \"Royal\" prefix in 1909; widely regarded as one of the best-preserved historic towns in the South East.",
        "nearby_towns": ["tonbridge", "sevenoaks", "dartford"],
        "planning_quirks": "Tunbridge Wells has extensive Article 4 Directions removing PD rights across its conservation areas. The High Weald AONB management plan applies tight controls on roof alterations, extensions and materials.",
    },
    "tonbridge": {
        "name": "Tonbridge",
        "county": "Kent",
        "council": "Tonbridge and Malling Borough Council",
        "postcodes": "TN9, TN10, TN11, TN12",
        "distance_from_london": "30 miles",
        "travel_time": "40 min from London Charing Cross",
        "typical_housing": "Medieval and Georgian buildings around the High Street and Castle, Victorian terraces by the station, interwar semis in Higham Wood and modern estates towards Hildenborough.",
        "conservation_notes": "Tonbridge Town, Hadlow, East Peckham and Hildenborough are conservation areas. Tonbridge Castle is a Scheduled Monument within the town centre.",
        "character": "Historic market town on the Medway, anchored by one of the best-preserved Norman castles in England.",
        "nearby_towns": ["tunbridge-wells", "sevenoaks", "dartford"],
        "planning_quirks": "Flood risk from the River Medway constrains much of the town centre. Tonbridge and Malling's Local Plan is under review, and large parts of the borough are Green Belt or Metropolitan Open Land.",
    },
    "dartford": {
        "name": "Dartford",
        "county": "Kent",
        "council": "Dartford Borough Council",
        "postcodes": "DA1, DA2",
        "distance_from_london": "17 miles",
        "travel_time": "45 min from London Charing Cross",
        "typical_housing": "Victorian terraces in West Hill and East Hill, 1930s semis across Wilmington and Joydens Wood, Thames-side warehouses converted to flats, and the large modern Ebbsfleet Garden City to the south-east.",
        "conservation_notes": "Dartford Town Centre, Stone and Sutton-at-Hone are conservation areas. The River Darent corridor is environmentally sensitive.",
        "character": "Thames Gateway regeneration town, gateway to the Dartford Crossing, with Ebbsfleet Garden City bringing major new housing supply.",
        "nearby_towns": ["gravesend", "sevenoaks", "tonbridge"],
        "planning_quirks": "Dartford sits within the Thames Gateway priority growth area. Large parts of the borough are within the Kent Downs AONB fringe and Green Belt. Contaminated-land screening applies across the former chalk quarries and industrial sites.",
    },
    "gravesend": {
        "name": "Gravesend",
        "county": "Kent",
        "council": "Gravesham Borough Council",
        "postcodes": "DA11, DA12, DA13",
        "distance_from_london": "21 miles",
        "travel_time": "23 min from London St Pancras (HS1)",
        "typical_housing": "Georgian and Victorian terraces in the old town, 1930s semis in Northfleet, modern estates at Singlewell, and rural cottages in the Green Belt villages to the south.",
        "conservation_notes": "Gravesend Town Centre, Milton Chantry and Cobham are conservation areas. Cobham Hall is a Grade I listed Elizabethan house.",
        "character": "Thames-side town with direct HS1 access to London, mixing historic riverside character with significant postwar suburban growth.",
        "nearby_towns": ["dartford", "tonbridge", "sevenoaks"],
        "planning_quirks": "Gravesham's Local Plan 2014 prioritises the rural Green Belt. Parts of the town sit within Flood Zones 2-3 from the Thames. Ebbsfleet Valley nearby is absorbing significant cross-borough growth.",
    },
    # ----- Buckinghamshire (3) -----
    "high-wycombe": {
        "name": "High Wycombe",
        "county": "Buckinghamshire",
        "council": "Buckinghamshire Council",
        "postcodes": "HP10, HP11, HP12, HP13",
        "distance_from_london": "30 miles",
        "travel_time": "28 min from London Marylebone",
        "typical_housing": "Victorian terraces in the town centre, Edwardian villas in Terriers, extensive 1930s and postwar semis across Totteridge and Micklefield, and rural cottages in the Chiltern villages.",
        "conservation_notes": "High Wycombe Town, Hughenden, West Wycombe and Penn are conservation areas. The entire district falls partly within the Chilterns National Landscape (AONB).",
        "character": "Largest town in Buckinghamshire, historically the furniture-making capital of England and home to Hughenden Manor (Disraeli's house).",
        "nearby_towns": ["amersham", "beaconsfield", "slough"],
        "planning_quirks": "Buckinghamshire Council's emerging Local Plan covers the whole unitary area, but Chilterns AONB status applies to much of High Wycombe's rural setting, triggering landscape and dark-sky policy tests on extensions.",
    },
    "amersham": {
        "name": "Amersham",
        "county": "Buckinghamshire",
        "council": "Buckinghamshire Council",
        "postcodes": "HP6, HP7",
        "distance_from_london": "27 miles",
        "travel_time": "35 min via Metropolitan line",
        "typical_housing": "Tudor and Georgian cottages in Old Amersham (one of England's best-preserved market towns), Edwardian Metro-land villas in Amersham-on-the-Hill, and interwar and modern estates on the periphery.",
        "conservation_notes": "Old Amersham, Amersham-on-the-Hill and Chesham Bois are conservation areas. Much of the parish is within the Chilterns AONB.",
        "character": "Split town: Old Amersham is a chocolate-box Tudor high street while Amersham-on-the-Hill is the archetypal Metro-land commuter suburb.",
        "nearby_towns": ["beaconsfield", "high-wycombe", "watford"],
        "planning_quirks": "Old Amersham has the tightest design controls in Buckinghamshire; many properties are listed Grade II or Grade II*. The Chilterns AONB applies across the southern parish and restricts height, massing and materials.",
    },
    "beaconsfield": {
        "name": "Beaconsfield",
        "county": "Buckinghamshire",
        "council": "Buckinghamshire Council",
        "postcodes": "HP9",
        "distance_from_london": "25 miles",
        "travel_time": "25 min from London Marylebone",
        "typical_housing": "Historic timber-framed and Georgian houses in Old Town, Edwardian Metro-land villas in New Town, and large detached executive homes on Ledborough Lane and Knotty Green.",
        "conservation_notes": "Beaconsfield Old Town and New Town are both conservation areas. Hall Barn and Wilton Park are Grade I and Grade II registered landscapes respectively.",
        "character": "Consistently ranked among the UK's most expensive towns by average property price; split into historic Old Town and Metro-land New Town.",
        "nearby_towns": ["amersham", "high-wycombe", "slough"],
        "planning_quirks": "Beaconsfield Old Town has Article 4 Direction and very strict conservation-area rules. The Chilterns AONB applies partially; Green Belt covers most of the rural setting.",
    },
    # ----- Berkshire (2) -----
    "slough": {
        "name": "Slough",
        "county": "Berkshire",
        "council": "Slough Borough Council",
        "postcodes": "SL1, SL2, SL3",
        "distance_from_london": "20 miles",
        "travel_time": "18 min from London Paddington (Elizabeth line)",
        "typical_housing": "Victorian terraces in Chalvey and Upton, extensive interwar semis across Cippenham and Langley, 1960s tower blocks in the town centre, and modern estates at Wexham.",
        "conservation_notes": "Upton, Ditton Park and Stoke Green are conservation areas. Upton Court is a Grade I listed building.",
        "character": "Densely populated unitary authority on the Elizabeth line; major commercial centre with significant ongoing residential intensification.",
        "nearby_towns": ["windsor", "staines-upon-thames", "high-wycombe"],
        "planning_quirks": "Slough has the highest population density in the South East outside London. Heathrow noise contours affect the south of the borough, and the Colnbrook/Poyle area is subject to PSZ restrictions. Article 4 removes HMO conversion PD rights borough-wide.",
    },
    "windsor": {
        "name": "Windsor",
        "county": "Berkshire",
        "council": "Royal Borough of Windsor and Maidenhead",
        "postcodes": "SL4",
        "distance_from_london": "23 miles",
        "travel_time": "55 min from London Waterloo",
        "typical_housing": "Georgian and Victorian townhouses in the town centre (all within sight of the castle), Edwardian and interwar villas in Dedworth and Clewer, and the large Eton Wick and Ascot fringes of substantial detached homes.",
        "conservation_notes": "Windsor Town Centre, Old Windsor, Datchet and Eton are conservation areas. Windsor Castle and the Long Walk are within the Windsor Great Park Grade I registered landscape.",
        "character": "Home of the oldest occupied castle in the world, a heavily protected historic town with exceptional tourist footfall.",
        "nearby_towns": ["slough", "staines-upon-thames", "beaconsfield"],
        "planning_quirks": "Heritage controls are unusually tight: views to and from Windsor Castle are protected by designated view corridors, and the Grade I listing of the castle triggers Historic England consultation on many nearby applications. Green Belt covers most of the rural parish.",
    },
    # ----- Bedfordshire (1) -----
    "luton": {
        "name": "Luton",
        "county": "Bedfordshire",
        "council": "Luton Borough Council",
        "postcodes": "LU1, LU2, LU3, LU4",
        "distance_from_london": "30 miles",
        "travel_time": "25 min from London St Pancras",
        "typical_housing": "Victorian and Edwardian terraces in Bury Park and High Town, interwar semis across Stopsley and Limbury, large postwar estates at Marsh Farm and Lewsey Farm, and modern apartments around the town centre.",
        "conservation_notes": "Plaiters Lea, Castle Street and Bury Park are conservation areas. Luton Hoo is a Grade I registered landscape just south of the town.",
        "character": "Unitary authority and home to Luton Airport; densely populated with significant ongoing regeneration around the station and the former Vauxhall plant.",
        "nearby_towns": ["st-albans", "hemel-hempstead", "welwyn-garden-city"],
        "planning_quirks": "Luton is tightly bounded and largely built-out; the Local Plan 2011-31 depends on cross-boundary co-operation with Central Bedfordshire for growth. Airport safeguarding zones, public safety zones and noise contours apply across significant areas of the borough.",
    },
    # ----- Oxfordshire (1) -----
    "oxford": {
        "name": "Oxford",
        "county": "Oxfordshire",
        "council": "Oxford City Council",
        "postcodes": "OX1, OX2, OX3, OX4",
        "distance_from_london": "55 miles",
        "travel_time": "55 min from London Paddington",
        "typical_housing": "Medieval college buildings and Georgian townhouses in the historic centre, Victorian terraces in Jericho and Cowley, Edwardian villas in North Oxford, and interwar and postwar estates in Headington, Blackbird Leys and Botley.",
        "conservation_notes": "Oxford has 17 conservation areas including the Central (University) area, North Oxford, Jericho, Park Town and Headington Hill. A large proportion of the centre is within the UNESCO World Heritage buffer-style \"High Buildings\" policy area.",
        "character": "UNESCO World Heritage candidate and home to the oldest English-speaking university in the world; exceptionally constrained by heritage and Green Belt.",
        "nearby_towns": ["high-wycombe", "amersham", "beaconsfield"],
        "planning_quirks": "Oxford's \"High Building Policy\" caps ridge heights across much of the city to protect the famous skyline of spires. The city is 95% constrained (Green Belt, flood risk, or conservation area). Article 4 Directions apply to HMO conversions citywide, with additional Article 4s on roof alterations across multiple wards.",
    },
}


# Verify the count (self-check during development)
assert len(TOWNS) == 30, f"Expected 30 towns, got {len(TOWNS)}"


# ---------------------------------------------------------------------------
# Shared HTML fragments
# ---------------------------------------------------------------------------
TICK_SVG = ('<svg viewBox="0 0 20 20" fill="currentColor" style="width:18px;height:18px;color:var(--success);flex-shrink:0;margin-top:2px;">'
            '<path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/>'
            '</svg>')


def gradient_hero(name, county):
    """Generate an inline SVG hero placeholder with the town name + county."""
    # Use an encoded inline SVG to guarantee visibility in all contexts
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 640" '
        f'preserveAspectRatio="xMidYMid slice" role="img" '
        f'aria-label="Architectural Drawings in {name}, {county}" '
        f'style="width:100%;height:100%;display:block;">'
        f'<defs>'
        f'<linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0%" stop-color="#F5E6DD"/>'
        f'<stop offset="55%" stop-color="#E8C6B2"/>'
        f'<stop offset="100%" stop-color="#C8664A"/>'
        f'</linearGradient>'
        f'<pattern id="p" width="80" height="80" patternUnits="userSpaceOnUse">'
        f'<path d="M0 80L80 0M-20 20L20 -20M60 100L100 60" stroke="rgba(255,255,255,0.12)" stroke-width="1"/>'
        f'</pattern>'
        f'</defs>'
        f'<rect width="1600" height="640" fill="url(#g)"/>'
        f'<rect width="1600" height="640" fill="url(#p)"/>'
        f'<g font-family="Fraunces, Georgia, serif" fill="#0E1116">'
        f'<text x="80" y="350" font-size="120" font-style="italic" font-weight="300">{name}</text>'
        f'<text x="84" y="420" font-size="36" font-weight="500" fill="#4A5260" font-family="Manrope, Helvetica, sans-serif" letter-spacing="8">{county.upper()}</text>'
        f'</g>'
        f'</svg>'
    )
    return svg


def nearby_town_cards(slugs, current_slug):
    """Return HTML grid for nearby/other towns linking to sibling hub pages."""
    cards = []
    for s in slugs:
        if s == current_slug:
            continue
        t = TOWNS.get(s)
        if not t:
            continue
        cards.append(
            f'<a href="../{s}/" style="display:block;padding:20px 22px;background:var(--surface);border:1px solid var(--line);border-radius:var(--r-md);text-decoration:none;transition:all 0.2s var(--ease);">'
            f'<div style="font-family:var(--font-display);font-size:1.2rem;color:var(--ink);font-variation-settings:\'opsz\' 60;">{t["name"]}</div>'
            f'<div style="color:var(--ink-soft);font-size:0.86rem;margin-top:4px;">{t["county"]} &middot; {t["distance_from_london"]} from London</div>'
            f'</a>'
        )
    return "\n".join(cards)


def all_towns_grid(current_slug=None, path_prefix="../"):
    """Return HTML for the full 30-town grid used at the bottom of every page."""
    cards = []
    for s, t in TOWNS.items():
        marker = ""
        if s == current_slug:
            marker = ' style="display:block;padding:14px 18px;background:var(--accent-soft);border:1px solid var(--accent);border-radius:var(--r-md);color:var(--accent-deep);font-weight:600;text-decoration:none;"'
            cards.append(
                f'<span{marker}>{t["name"]} (this page)</span>'
            )
        else:
            cards.append(
                f'<a href="{path_prefix}{s}/" style="display:block;padding:14px 18px;background:var(--surface);border:1px solid var(--line);border-radius:var(--r-md);color:var(--ink);font-weight:500;text-decoration:none;transition:all 0.2s var(--ease);font-size:0.94rem;">{t["name"]} <span style="color:var(--ink-softer);font-weight:400;font-size:0.84rem;">&middot; {t["county"]}</span></a>'
            )
    return "\n".join(cards)


def faq_schema(faqs):
    """Build FAQPage JSON-LD from list of (question, answer) tuples."""
    items = []
    for q, a in faqs:
        q_esc = q.replace('"', '\\"')
        a_esc = a.replace('"', '\\"').replace("\n", " ")
        items.append(
            f'    {{"@type": "Question", "name": "{q_esc}", '
            f'"acceptedAnswer": {{"@type": "Answer", "text": "{a_esc}"}}}}'
        )
    return ",\n".join(items)


# ---------------------------------------------------------------------------
# Service cards (5 services, identical everywhere)
# ---------------------------------------------------------------------------
def service_cards(town_name):
    services = [
        ("Planning Permission Drawings", "planning-drawings",
         "Full planning submission: existing/proposed plans, elevations, site plan, and Design &amp; Access Statement.",
         "from &pound;840", "Essentials"),
        ("Building Regulations Drawings", "building-regulations",
         "Construction-detail drawings for your builder and Building Control submission.",
         "from &pound;1,750", "Complete"),
        ("Loft Conversion Drawings", "loft-conversions",
         "Rear dormer, hip-to-gable, L-shape or mansard loft conversion drawings.",
         "from &pound;1,225", "Loft package"),
        ("House Extension Plans", "house-extensions",
         "Single-storey, double-storey, wrap-around and side-return extension drawings.",
         "from &pound;840", "Essentials"),
        ("Mansard Roof Extensions", "mansard-roof",
         "Full mansard conversion drawings with structural and thermal detailing.",
         "from &pound;1,575", "Mansard package"),
    ]
    cards = []
    for title, slug, desc, price, tier in services:
        cards.append(
            f'<a href="../../../services/{slug}.html" class="service-card reveal" style="text-decoration:none;color:inherit;">'
            f'<div class="service-card-icon" style="width:44px;height:44px;border-radius:12px;background:var(--accent-soft);display:grid;place-items:center;margin-bottom:18px;">'
            f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" style="width:22px;height:22px;color:var(--accent-deep);"><path d="M3 7h18M3 12h18M3 17h12"/></svg>'
            f'</div>'
            f'<h3 style="font-family:var(--font-display);font-size:1.35rem;font-variation-settings:\'opsz\' 60;margin-bottom:10px;">{title} in {town_name}</h3>'
            f'<p style="color:var(--ink-soft);font-size:0.98rem;line-height:1.55;margin-bottom:16px;">{desc}</p>'
            f'<div style="display:flex;justify-content:space-between;align-items:center;padding-top:14px;border-top:1px solid var(--line);">'
            f'<span style="font-family:var(--font-display);font-size:1.1rem;font-variation-settings:\'opsz\' 36;">{price}</span>'
            f'<span style="font-size:0.82rem;color:var(--accent-deep);font-weight:600;text-transform:uppercase;letter-spacing:0.1em;">{tier} &rarr;</span>'
            f'</div>'
            f'</a>'
        )
    return "\n".join(cards)


# ---------------------------------------------------------------------------
# Page template
# ---------------------------------------------------------------------------
def generate_page(slug, t):
    name = t["name"]
    county = t["county"]
    council = t["council"]
    postcodes = t["postcodes"]
    distance = t["distance_from_london"]
    travel = t["travel_time"]
    housing = t["typical_housing"]
    conservation_notes = t["conservation_notes"]
    character = t["character"]
    nearby = t["nearby_towns"]
    quirks = t["planning_quirks"]

    # ---- SEO meta ----
    title = f"Architectural Drawings in {name} | MCIAT Chartered | AD London"
    if len(title) > 72:
        title = f"Architectural Drawings {name} | MCIAT Chartered | AD"
    meta_desc = (
        f"MCIAT-chartered architectural drawings in {name}, {county}. "
        f"Planning permission, building regulations, loft conversions and extensions. "
        f"Fixed fees from &pound;840, 30% below London rates."
    )
    meta_desc_clean = meta_desc.replace("&pound;", "\u00a3")
    if len(meta_desc_clean) > 160:
        meta_desc_clean = meta_desc_clean[:157] + "..."

    canonical = f"https://www.architecturaldrawings.uk/areas/commuter/{slug}/"

    # ---- FAQ ----
    faqs = [
        (
            f"Do you cover {name}?",
            f"Yes. {name} is well within our 50-mile service radius from our London office. "
            f"We cover all {name} postcodes ({postcodes}) for planning permission drawings, "
            f"building regulations drawings, loft conversions, house extensions and mansard "
            f"roofs. {name} is {distance} from central London ({travel}), so our team can "
            f"comfortably visit for measured surveys and pre-application meetings with "
            f"{council}."
        ),
        (
            f"How much do architectural drawings cost in {name}?",
            f"Our fixed fees in {name} match our London rates: Essentials from \u00a3840 "
            f"(planning drawings only), Complete from \u00a31,750 (planning + building "
            f"regulations), Loft package from \u00a31,225, and Mansard package from "
            f"\u00a31,575. These prices are roughly 30% below typical London architect rates "
            f"for the same scope of work. {council} application fees are charged separately "
            f"at the statutory rate (\u00a3258 for a householder planning application, \u00a3129 "
            f"for a Lawful Development Certificate in 2026)."
        ),
        (
            f"Do you visit the site in {name}?",
            f"Yes, every project includes an in-person measured survey at your property in "
            f"{name}. Travel time from London is included in our fixed fee \u2014 you will "
            f"never be charged mileage or hourly rates for site visits. We typically combine "
            f"the measured survey with an initial brief discussion on site, then return for "
            f"pre-submission checks if needed. For projects that require pre-application "
            f"meetings at {council}, we attend on your behalf and include the call or meeting "
            f"in the fee."
        ),
        (
            f"Can you work with {council}?",
            f"Yes. While our office is in London, our MCIAT chartered architectural "
            f"technologists regularly submit to councils across the M25 commuter belt, "
            f"including {council}. We use the Planning Portal for submissions, so the "
            f"process is identical regardless of which local planning authority handles your "
            f"application. We research each council's Local Plan, design guides, and recent "
            f"decision history before preparing your drawings so that the scheme aligns "
            f"with their current approach."
        ),
        (
            f"How long does {council} take to decide a planning application?",
            f"The statutory target for a householder planning application is 8 weeks from "
            f"validation. {council} generally meets this target for straightforward "
            f"applications, although conservation area or listed building consents can take "
            f"longer. Pre-application advice typically takes 4\u20136 weeks. From initial "
            f"instruction to final decision, expect 10\u201316 weeks for a typical residential "
            f"project in {name}."
        ),
    ]
    faq_json = faq_schema(faqs)

    faq_html_items = []
    for q, a in faqs:
        faq_html_items.append(
            f'      <details class="faq-item">\n'
            f'        <summary>\n'
            f'          {q}\n'
            f'          <span class="faq-icon"><svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2"><path d="M8 3v10M3 8h10"/></svg></span>\n'
            f'        </summary>\n'
            f'        <div class="faq-answer">\n'
            f'          <p>{a}</p>\n'
            f'        </div>\n'
            f'      </details>'
        )
    faq_html = "\n\n".join(faq_html_items)

    # ---- Pricing tiers ----
    pricing_cards = (
        f'<div class="pricing-card reveal" style="background:var(--surface);border:1px solid var(--line);border-radius:var(--r-lg);padding:32px 28px;">'
        f'<h3 style="font-family:var(--font-display);font-size:1.6rem;margin-bottom:6px;">Essentials</h3>'
        f'<p style="color:var(--ink-soft);font-size:0.92rem;margin-bottom:20px;">Planning permission drawings for {name}.</p>'
        f'<div style="font-family:var(--font-display);font-size:2.6rem;font-variation-settings:\'opsz\' 72;color:var(--ink);margin-bottom:4px;">&pound;840</div>'
        f'<div style="color:var(--ink-soft);font-size:0.88rem;margin-bottom:24px;">fixed fee &middot; incl. measured survey &middot; travel to {name} included</div>'
        f'<ul style="list-style:none;padding:0;display:flex;flex-direction:column;gap:10px;">'
        f'<li style="display:flex;gap:10px;font-size:0.95rem;">{TICK_SVG}<span>Existing and proposed plans</span></li>'
        f'<li style="display:flex;gap:10px;font-size:0.95rem;">{TICK_SVG}<span>Existing and proposed elevations</span></li>'
        f'<li style="display:flex;gap:10px;font-size:0.95rem;">{TICK_SVG}<span>Block plan &amp; location plan</span></li>'
        f'<li style="display:flex;gap:10px;font-size:0.95rem;">{TICK_SVG}<span>Design &amp; Access Statement where required</span></li>'
        f'<li style="display:flex;gap:10px;font-size:0.95rem;">{TICK_SVG}<span>{council} submission via Planning Portal</span></li>'
        f'</ul>'
        f'<a href="../../../quote.html?service=planning&amp;tier=essentials&amp;location={slug}" class="btn btn-outline" style="margin-top:28px;width:100%;justify-content:center;">Get an Essentials quote</a>'
        f'</div>'
        f'<div class="pricing-card popular reveal" style="background:var(--ink);color:#fff;border:1px solid var(--ink);border-radius:var(--r-lg);padding:32px 28px;position:relative;">'
        f'<span style="position:absolute;top:-14px;left:28px;background:var(--accent);color:#fff;padding:6px 14px;border-radius:var(--r-full);font-size:0.72rem;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;">Most popular</span>'
        f'<h3 style="font-family:var(--font-display);font-size:1.6rem;margin-bottom:6px;">Complete</h3>'
        f'<p style="color:rgba(255,255,255,0.7);font-size:0.92rem;margin-bottom:20px;">Planning + building regulations drawings for {name}.</p>'
        f'<div style="font-family:var(--font-display);font-size:2.6rem;font-variation-settings:\'opsz\' 72;color:#fff;margin-bottom:4px;">&pound;1,750</div>'
        f'<div style="color:rgba(255,255,255,0.6);font-size:0.88rem;margin-bottom:24px;">fixed fee &middot; planning &amp; build-ready drawings</div>'
        f'<ul style="list-style:none;padding:0;display:flex;flex-direction:column;gap:10px;">'
        f'<li style="display:flex;gap:10px;font-size:0.95rem;"><svg viewBox="0 0 20 20" fill="currentColor" style="width:18px;height:18px;color:var(--accent);flex-shrink:0;margin-top:2px;"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg><span>Everything in Essentials</span></li>'
        f'<li style="display:flex;gap:10px;font-size:0.95rem;"><svg viewBox="0 0 20 20" fill="currentColor" style="width:18px;height:18px;color:var(--accent);flex-shrink:0;margin-top:2px;"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg><span>Full building regulations package</span></li>'
        f'<li style="display:flex;gap:10px;font-size:0.95rem;"><svg viewBox="0 0 20 20" fill="currentColor" style="width:18px;height:18px;color:var(--accent);flex-shrink:0;margin-top:2px;"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg><span>Construction sections and details</span></li>'
        f'<li style="display:flex;gap:10px;font-size:0.95rem;"><svg viewBox="0 0 20 20" fill="currentColor" style="width:18px;height:18px;color:var(--accent);flex-shrink:0;margin-top:2px;"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg><span>Structural coordination</span></li>'
        f'<li style="display:flex;gap:10px;font-size:0.95rem;"><svg viewBox="0 0 20 20" fill="currentColor" style="width:18px;height:18px;color:var(--accent);flex-shrink:0;margin-top:2px;"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg><span>Building Control submission</span></li>'
        f'</ul>'
        f'<a href="../../../quote.html?service=extension&amp;tier=complete&amp;location={slug}" class="btn btn-primary" style="margin-top:28px;width:100%;justify-content:center;background:var(--accent);color:#fff;">Get a Complete quote</a>'
        f'</div>'
        f'<div class="pricing-card reveal" style="background:var(--surface);border:1px solid var(--line);border-radius:var(--r-lg);padding:32px 28px;">'
        f'<h3 style="font-family:var(--font-display);font-size:1.6rem;margin-bottom:6px;">Bespoke</h3>'
        f'<p style="color:var(--ink-soft);font-size:0.92rem;margin-bottom:20px;">Complex or listed-building projects in {name}.</p>'
        f'<div style="font-family:var(--font-display);font-size:2.6rem;font-variation-settings:\'opsz\' 72;color:var(--ink);margin-bottom:4px;">Quote</div>'
        f'<div style="color:var(--ink-soft);font-size:0.88rem;margin-bottom:24px;">pricing tailored to project scope</div>'
        f'<ul style="list-style:none;padding:0;display:flex;flex-direction:column;gap:10px;">'
        f'<li style="display:flex;gap:10px;font-size:0.95rem;">{TICK_SVG}<span>Listed building consent applications</span></li>'
        f'<li style="display:flex;gap:10px;font-size:0.95rem;">{TICK_SVG}<span>Heritage statements &amp; conservation reports</span></li>'
        f'<li style="display:flex;gap:10px;font-size:0.95rem;">{TICK_SVG}<span>Basement conversions</span></li>'
        f'<li style="display:flex;gap:10px;font-size:0.95rem;">{TICK_SVG}<span>New-build dwellings &amp; self-build</span></li>'
        f'<li style="display:flex;gap:10px;font-size:0.95rem;">{TICK_SVG}<span>Commercial &amp; change-of-use projects</span></li>'
        f'</ul>'
        f'<a href="../../../quote.html?service=bespoke&amp;location={slug}" class="btn btn-outline" style="margin-top:28px;width:100%;justify-content:center;">Request a Bespoke quote</a>'
        f'</div>'
    )

    # ---- Typical projects paragraph (contextual to housing) ----
    hl = housing.lower()
    typical_projects = []
    if "terrace" in hl:
        typical_projects.append(
            f"<p><strong>Rear and side-return extensions</strong> on {name}'s Victorian and "
            f"Edwardian terraces are among the most common projects we handle. A single-storey "
            f"rear extension of up to 6 metres is often achievable without full planning "
            f"permission, though conservation-area status (see {council} guidance) typically "
            f"removes Permitted Development rights.</p>"
        )
    if "semi" in hl:
        typical_projects.append(
            f"<p><strong>Two-storey side and rear extensions</strong> on {name}'s 1930s "
            f"semi-detached housing stock allow for a larger kitchen and dining area at "
            f"ground floor and an additional bedroom and bathroom above. {council} generally "
            f"supports subordinate extensions that maintain the original house's form and "
            f"street rhythm.</p>"
        )
    if "detach" in hl or "executive" in hl:
        typical_projects.append(
            f"<p><strong>Wrap-around extensions and garage conversions</strong> on the larger "
            f"detached houses in {name} are popular for creating open-plan family kitchens "
            f"and home offices. These projects often combine planning permission, building "
            f"regulations approval and structural calculations \u2014 all covered within our "
            f"Complete package.</p>"
        )
    if "cottage" in hl or "medieval" in hl or "tudor" in hl or "georgian" in hl:
        typical_projects.append(
            f"<p><strong>Sympathetic extensions to listed and historic homes</strong> require "
            f"additional heritage input. For period properties in {name}, we prepare heritage "
            f"impact statements, use traditional materials and maintain the original "
            f"proportions that {council}'s conservation officer will expect to see.</p>"
        )
    if "new town" in hl or "postwar" in hl or "1950s" in hl or "1960s" in hl or "estate" in hl or "radburn" in hl:
        typical_projects.append(
            f"<p><strong>Rear extensions and loft conversions</strong> on {name}'s post-war "
            f"and New Town estates unlock significant additional living space. Many of these "
            f"houses were built with low floor-to-ceiling heights, so we carry out a careful "
            f"head-height survey before confirming loft-conversion feasibility.</p>"
        )
    if "flat" in hl or "apartment" in hl or "tower" in hl:
        typical_projects.append(
            f"<p><strong>Internal reconfigurations and flat conversions</strong> are common "
            f"for the apartment stock in central {name}. These rarely need planning "
            f"permission but do require building regulations and often Party Wall "
            f"notifications, which we can coordinate as part of the project.</p>"
        )
    if not typical_projects:
        typical_projects.append(
            f"<p>Typical projects in {name} include rear and side extensions, loft "
            f"conversions, garage conversions and whole-house refurbishments. We prepare "
            f"the planning drawings, building regulations drawings and supporting "
            f"documentation required by {council} for all of these.</p>"
        )

    typical_html = "\n".join(typical_projects)

    # ---- Nearby towns grid ----
    nearby_html = nearby_town_cards(nearby, slug)

    # ---- All commuter towns grid (for internal linking) ----
    all_grid = all_towns_grid(current_slug=slug, path_prefix="../")

    # ---- Hero SVG ----
    hero_svg = gradient_hero(name, county)

    # ---- Build full HTML ----
    html = f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8" />
<link rel="alternate" hreflang="en-GB" href="https://www.architecturaldrawings.uk/" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{title}</title>
<meta name="description" content="{meta_desc_clean}" />
<link rel="author" href="/team/" />
<link rel="canonical" href="{canonical}" />

<!-- Open Graph -->
<meta property="og:type" content="website" />
<meta property="og:url" content="{canonical}" />
<meta property="og:title" content="Architectural Drawings in {name}, {county}" />
<meta property="og:description" content="{meta_desc_clean}" />
<meta property="og:locale" content="en_GB" />
<meta property="og:site_name" content="Architectural Drawings London" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="Architectural Drawings in {name}, {county}" />
<meta name="twitter:description" content="{meta_desc_clean}" />

<!-- Service schema -->
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "Architectural Drawings in {name}",
  "description": "MCIAT-chartered architectural drawings service covering {name}, {county}. Planning permission, building regulations, loft conversions, house extensions and mansard roofs from a London base within our 50-mile service radius.",
  "provider": {{
    "@type": "Organization",
    "name": "Architectural Drawings London",
    "url": "https://www.architecturaldrawings.uk",
    "telephone": "+44-20-7946-0000",
    "address": {{
      "@type": "PostalAddress",
      "streetAddress": "86\u201390 Paul Street",
      "addressLocality": "London",
      "postalCode": "EC2A 4NE",
      "addressCountry": "GB"
    }}
  }},
  "areaServed": {{
    "@type": "Place",
    "name": "{name}, {county}",
    "address": {{
      "@type": "PostalAddress",
      "addressLocality": "{name}",
      "addressRegion": "{county}",
      "addressCountry": "GB"
    }}
  }},
  "url": "{canonical}",
  "offers": [
    {{ "@type": "Offer", "name": "Essentials", "price": "840", "priceCurrency": "GBP" }},
    {{ "@type": "Offer", "name": "Complete", "price": "1750", "priceCurrency": "GBP" }},
    {{ "@type": "Offer", "name": "Loft", "price": "1225", "priceCurrency": "GBP" }},
    {{ "@type": "Offer", "name": "Mansard", "price": "1575", "priceCurrency": "GBP" }}
  ]
}}
</script>

<!-- LocalBusiness schema -->
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "@id": "https://www.architecturaldrawings.uk/#business-{slug}",
  "name": "Architectural Drawings London \u2014 {name}",
  "image": "https://www.architecturaldrawings.uk/assets/img/hero-1600.jpg",
  "url": "{canonical}",
  "telephone": "+44-20-7946-0000",
  "priceRange": "\u00a3840\u2013\u00a35000",
  "address": {{
    "@type": "PostalAddress",
    "streetAddress": "86\u201390 Paul Street",
    "addressLocality": "London",
    "postalCode": "EC2A 4NE",
    "addressCountry": "GB"
  }},
  "areaServed": [
    {{ "@type": "Place", "name": "{name}" }},
    {{ "@type": "Place", "name": "{county}" }}
  ]
}}
</script>

<!-- BreadcrumbList schema -->
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.architecturaldrawings.uk/" }},
    {{ "@type": "ListItem", "position": 2, "name": "Areas we cover", "item": "https://www.architecturaldrawings.uk/areas/" }},
    {{ "@type": "ListItem", "position": 3, "name": "Commuter belt", "item": "https://www.architecturaldrawings.uk/areas/commuter/" }},
    {{ "@type": "ListItem", "position": 4, "name": "{name}", "item": "{canonical}" }}
  ]
}}
</script>

<!-- FAQPage schema -->
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
{faq_json}
  ]
}}
</script>

<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,200..900,0..100;1,9..144,200..900,0..100&family=Manrope:wght@300;400;500;600;700;800&display=swap" />
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,200..900,0..100;1,9..144,200..900,0..100&family=Manrope:wght@300;400;500;600;700;800&display=swap" media="print" onload="this.media='all'" />
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,200..900,0..100;1,9..144,200..900,0..100&family=Manrope:wght@300;400;500;600;700;800&display=swap" /></noscript>
<link rel="stylesheet" href="/assets/css/style.css" />

<style>
{css_escaped}

/* Commuter-belt specific tweaks */
.commuter-hero {{
  position: relative;
  border-radius: var(--r-xl);
  overflow: hidden;
  aspect-ratio: 25 / 10;
  background: var(--bg-2);
  margin-bottom: 40px;
}}
.commuter-hero > svg {{ position: absolute; inset: 0; width: 100%; height: 100%; }}
.badge-pill {{
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 14px;
  border-radius: var(--r-full);
  background: var(--accent-soft);
  color: var(--accent-deep);
  font-size: 0.82rem;
  font-weight: 600;
  letter-spacing: 0.04em;
}}
.breadcrumbs {{
  font-size: 0.84rem;
  color: var(--ink-soft);
  margin-bottom: 24px;
}}
.breadcrumbs a {{ color: var(--ink-soft); text-decoration: none; font-weight: 500; }}
.breadcrumbs a:hover {{ color: var(--accent-deep); }}
.breadcrumbs span {{ margin: 0 6px; opacity: 0.5; }}

.tldr-box {{
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: var(--r-lg);
  padding: 28px 32px;
  margin: 0 0 48px;
}}
.tldr-box h4 {{
  font-family: var(--font-body);
  font-size: 0.78rem;
  font-weight: 600;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--accent-deep);
  margin: 0 0 16px;
}}
.tldr-box ul {{
  list-style: none; margin: 0; padding: 0;
  display: flex; flex-direction: column; gap: 10px;
}}
.tldr-box li {{ font-size: 0.95rem; display: flex; align-items: flex-start; gap: 10px; line-height: 1.5; }}

.service-grid {{
  display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 20px;
}}
.service-card {{
  background: var(--surface); border: 1px solid var(--line);
  border-radius: var(--r-lg); padding: 28px;
  transition: all 0.3s var(--ease);
}}
.service-card:hover {{ transform: translateY(-4px); box-shadow: var(--shadow-glow); border-color: var(--accent-soft); }}

.pricing-grid {{
  display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
}}

.faq-list {{ display: flex; flex-direction: column; }}
.faq-item {{ border-top: 1px solid var(--line-strong); }}
.faq-item:last-child {{ border-bottom: 1px solid var(--line-strong); }}
.faq-item summary {{
  width: 100%; padding: 24px 0;
  display: flex; justify-content: space-between; align-items: center; gap: 20px;
  font-family: var(--font-display); font-size: 1.15rem; font-variation-settings: 'opsz' 60;
  cursor: pointer; list-style: none;
}}
.faq-item summary::-webkit-details-marker {{ display: none; }}
.faq-item summary:hover {{ color: var(--accent-deep); }}
.faq-item .faq-icon {{
  width: 28px; height: 28px; border-radius: 50%;
  border: 1px solid var(--line-strong);
  display: grid; place-items: center; flex-shrink: 0;
  transition: transform 0.3s var(--ease-spring), background 0.3s var(--ease); color: var(--ink-soft);
}}
.faq-item[open] .faq-icon {{ transform: rotate(45deg); background: var(--accent); color: #fff; border-color: var(--accent); }}
.faq-item .faq-answer {{ padding: 0 0 24px; color: var(--ink-soft); font-size: 0.98rem; line-height: 1.65; }}

.footer {{ background: var(--ink); color: rgba(250,250,247,0.6); }}
.footer .logo {{ color: var(--bg); }}
.footer .logo-mark {{ background: var(--bg); color: var(--ink); }}
.footer-col p, .footer-col h5 {{ color: rgba(250,250,247,0.5); }}
.footer-col a {{ color: rgba(250,250,247,0.6); }}
.footer-col a:hover {{ color: var(--accent); }}
.footer-bottom {{ border-top-color: rgba(255,255,255,0.1); color: rgba(250,250,247,0.5); }}

/* Fail-safe reveal (works even if JS never runs) */
@keyframes __ad_safety_in {{ to {{ opacity: 1; transform: none; }} }}
.reveal {{ animation: __ad_safety_in 0.01s linear 1.5s forwards; }}
.reveal.in {{ animation: none; opacity: 1; transform: none; }}
</style>
</head>
<body>

<header class="nav" id="nav">
  <div class="container nav-inner">
    <a href="../../../" class="logo"><span class="logo-mark">A</span><span>Architectural<span style="color:var(--accent);font-style:italic;font-weight:400;"> Drawings</span></span></a>
    <nav><ul class="nav-links">
      <li><a href="../../../services.html">Services</a></li>
      <li><a href="../../../pricing.html">Pricing</a></li>
      <li><a href="../../../index.html#process">Process</a></li>
      <li><a href="../../../about.html">About</a></li>
    </ul></nav>
    <div class="nav-cta">
      <a href="../../../portal/login.html" class="btn btn-ghost btn-sm">Sign in</a>
      <a href="../../../quote.html" class="btn btn-primary btn-sm">Free quote</a>
    </div>
  </div>
</header>

<!-- ========================================================== -->
<!-- 1. Hero                                                    -->
<!-- ========================================================== -->
<section class="hero" style="padding-bottom: clamp(20px, 4vw, 40px);">
  <div class="container" style="max-width: 1100px;">
    <nav class="breadcrumbs">
      <a href="../../../">Home</a><span>/</span><a href="../../">Areas</a><span>/</span><a href="../">Commuter belt</a><span>/</span>{name}
    </nav>
    <div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:16px;">
      <span class="badge-pill">{county}</span>
      <span class="badge-pill" style="background:var(--bg-2);color:var(--ink-soft);">{distance} from London</span>
      <span class="badge-pill" style="background:var(--bg-2);color:var(--ink-soft);">{travel}</span>
    </div>
    <h1 style="margin: 8px 0 20px; font-size: clamp(2.4rem, 5.5vw, 4.2rem);">Architectural Drawings in <em style="color: var(--accent); font-weight: 300;">{name}</em></h1>
    <p style="max-width: 720px; font-size: 1.15rem; color: var(--ink-soft); line-height: 1.6; margin-bottom: 32px;">
      MCIAT chartered architectural technologists covering {name} and the wider {county} commuter belt from our London base.
      Planning permission, building regulations, loft conversions, extensions and mansard roofs \u2014 fixed fees from &pound;840, 30% below typical London architect rates.
    </p>
    <div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom: 40px;">
      <a href="../../../quote.html?location={slug}" class="btn btn-primary btn-lg">Get a free {name} quote &rarr;</a>
      <a href="../../../pricing.html" class="btn btn-outline btn-lg">See pricing</a>
    </div>
    <div class="commuter-hero reveal">
      {hero_svg}
    </div>
  </div>
</section>

<!-- ========================================================== -->
<!-- 2. TL;DR                                                   -->
<!-- ========================================================== -->
<section style="padding-top: 0;">
  <div class="container" style="max-width: 1100px;">
    <div class="tldr-box reveal">
      <h4>TL;DR &mdash; {name} at a glance</h4>
      <ul>
        <li>{TICK_SVG}<span><strong>Local planning authority:</strong> {council}</span></li>
        <li>{TICK_SVG}<span><strong>Postcodes covered:</strong> {postcodes}</span></li>
        <li>{TICK_SVG}<span><strong>Our fees:</strong> Essentials from &pound;840, Complete from &pound;1,750, Loft from &pound;1,225, Mansard from &pound;1,575</span></li>
        <li>{TICK_SVG}<span><strong>Distance from London:</strong> {distance} ({travel})</span></li>
        <li>{TICK_SVG}<span><strong>Site visits:</strong> included in the fee, no mileage or hourly charges</span></li>
        <li>{TICK_SVG}<span><strong>Credentials:</strong> MCIAT chartered, 98% first-time approval rate across all 33 London boroughs and M25 commuter belt</span></li>
      </ul>
    </div>
  </div>
</section>

<!-- ========================================================== -->
<!-- 3. Planning in {name}                                       -->
<!-- ========================================================== -->
<section style="padding-top: 24px;">
  <div class="container" style="max-width: 880px;">
    <span class="eyebrow">Local planning context</span>
    <h2 style="font-size: clamp(2rem, 4vw, 3rem); margin: 12px 0 20px;">Planning in {name}</h2>
    <p style="font-size: 1.05rem; line-height: 1.7; color: var(--ink); margin-bottom: 20px;">
      {character}
    </p>
    <p style="font-size: 1.05rem; line-height: 1.7; color: var(--ink); margin-bottom: 20px;">
      All householder planning applications in {name} are determined by <strong>{council}</strong>. The council follows the National Planning Policy Framework and its own adopted Local Plan, supported by area-specific design guides and Supplementary Planning Documents.
    </p>
    <p style="font-size: 1.05rem; line-height: 1.7; color: var(--ink); margin-bottom: 20px;">
      <strong>Conservation areas:</strong> {conservation_notes}
    </p>
    <p style="font-size: 1.05rem; line-height: 1.7; color: var(--ink); margin-bottom: 20px;">
      <strong>Policy quirks to watch:</strong> {quirks}
    </p>
    <p style="font-size: 1.05rem; line-height: 1.7; color: var(--ink); margin-bottom: 20px;">
      Typical housing in {name} includes {housing[0].lower()}{housing[1:]} This mix drives the types of projects we most often prepare drawings for here.
    </p>
  </div>
</section>

<!-- ========================================================== -->
<!-- 4. Our services in {name}                                   -->
<!-- ========================================================== -->
<section style="background: var(--bg-2);">
  <div class="container" style="max-width: 1100px;">
    <div style="max-width: 720px; margin-bottom: 40px;">
      <span class="eyebrow">Services in {name}</span>
      <h2 style="font-size: clamp(2rem, 4vw, 3rem); margin: 12px 0 16px;">Everything we cover in <em style="color: var(--accent); font-weight: 300;">{name}</em></h2>
      <p style="color: var(--ink-soft); font-size: 1.05rem; line-height: 1.6;">
        Five core services \u2014 all fixed-fee, all delivered by MCIAT chartered architectural technologists, all within our 50-mile service radius.
      </p>
    </div>
    <div class="service-grid">
      {service_cards(name)}
    </div>
  </div>
</section>

<!-- ========================================================== -->
<!-- 5. Why a London-based chartered practice                   -->
<!-- ========================================================== -->
<section>
  <div class="container" style="max-width: 880px;">
    <span class="eyebrow">Why choose us</span>
    <h2 style="font-size: clamp(2rem, 4vw, 3rem); margin: 12px 0 28px;">Why use a London-based chartered practice in {name}?</h2>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 24px;">
      <div class="reveal" style="background: var(--surface); border: 1px solid var(--line); border-radius: var(--r-lg); padding: 28px;">
        <h3 style="font-family: var(--font-display); font-size: 1.25rem; margin-bottom: 12px;">MCIAT chartered</h3>
        <p style="color: var(--ink-soft); font-size: 0.98rem; line-height: 1.6;">Every drawing is signed off by a Chartered Member of the Institute of Architectural Technologists. The same quality bar that applies to our central London projects applies to our {name} work.</p>
      </div>
      <div class="reveal" style="background: var(--surface); border: 1px solid var(--line); border-radius: var(--r-lg); padding: 28px;">
        <h3 style="font-family: var(--font-display); font-size: 1.25rem; margin-bottom: 12px;">Experience with out-of-London councils</h3>
        <p style="color: var(--ink-soft); font-size: 0.98rem; line-height: 1.6;">We regularly submit to all M25 commuter-belt councils including {council}. We research each council's Local Plan, design guides and recent decision history before we start drawing.</p>
      </div>
      <div class="reveal" style="background: var(--surface); border: 1px solid var(--line); border-radius: var(--r-lg); padding: 28px;">
        <h3 style="font-family: var(--font-display); font-size: 1.25rem; margin-bottom: 12px;">Travel included</h3>
        <p style="color: var(--ink-soft); font-size: 0.98rem; line-height: 1.6;">Site visits, measured surveys and pre-application meetings in {name} are all included in our fixed fee. No mileage charges, no hourly rates, no surprises on the invoice.</p>
      </div>
      <div class="reveal" style="background: var(--surface); border: 1px solid var(--line); border-radius: var(--r-lg); padding: 28px;">
        <h3 style="font-family: var(--font-display); font-size: 1.25rem; margin-bottom: 12px;">98% first-time approval</h3>
        <p style="color: var(--ink-soft); font-size: 0.98rem; line-height: 1.6;">Our submissions across the 33 London boroughs and the M25 commuter belt are approved at first application 98% of the time. Saving you the council resubmission fee and weeks of delay.</p>
      </div>
    </div>
  </div>
</section>

<!-- ========================================================== -->
<!-- 6. Typical projects in {name}                              -->
<!-- ========================================================== -->
<section style="background: var(--bg-2);">
  <div class="container" style="max-width: 880px;">
    <span class="eyebrow">Projects</span>
    <h2 style="font-size: clamp(2rem, 4vw, 3rem); margin: 12px 0 24px;">Typical {name} projects</h2>
    <div style="font-size: 1.05rem; line-height: 1.7; color: var(--ink);">
      {typical_html}
    </div>
  </div>
</section>

<!-- ========================================================== -->
<!-- 7. Pricing for {name}                                      -->
<!-- ========================================================== -->
<section>
  <div class="container" style="max-width: 1100px;">
    <div style="max-width: 720px; margin-bottom: 40px;">
      <span class="eyebrow">Fixed fees</span>
      <h2 style="font-size: clamp(2rem, 4vw, 3rem); margin: 12px 0 16px;">Pricing for {name}</h2>
      <p style="color: var(--ink-soft); font-size: 1.05rem; line-height: 1.6;">
        Same fixed fees as our London work \u2014 no "commuter belt premium", no hourly surprises. {council} application fees are charged separately at the statutory rate.
      </p>
    </div>
    <div class="pricing-grid">
      {pricing_cards}
    </div>
  </div>
</section>

<!-- ========================================================== -->
<!-- 8. FAQ                                                     -->
<!-- ========================================================== -->
<section style="background: var(--bg-2);">
  <div class="container" style="max-width: 860px;">
    <span class="eyebrow">FAQ</span>
    <h2 style="font-size: clamp(2rem, 4vw, 3rem); margin: 12px 0 32px;">Frequently asked questions &mdash; {name}</h2>
    <div class="faq-list">
{faq_html}
    </div>
  </div>
</section>

<!-- ========================================================== -->
<!-- 9. Nearby commuter towns                                   -->
<!-- ========================================================== -->
<section>
  <div class="container" style="max-width: 1100px;">
    <span class="eyebrow">Nearby commuter towns</span>
    <h2 style="font-size: clamp(1.8rem, 3.5vw, 2.6rem); margin: 12px 0 28px;">Other towns near {name}</h2>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px;">
      {nearby_html}
    </div>
  </div>
</section>

<!-- ========================================================== -->
<!-- 10. All 30 commuter towns (internal linking)               -->
<!-- ========================================================== -->
<section style="background: var(--bg-2);">
  <div class="container" style="max-width: 1100px;">
    <span class="eyebrow">All commuter towns we cover</span>
    <h2 style="font-size: clamp(1.8rem, 3.5vw, 2.6rem); margin: 12px 0 28px;">The complete M25 commuter belt</h2>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 12px;">
      {all_grid}
    </div>
  </div>
</section>

<!-- ========================================================== -->
<!-- 11. CTA band                                               -->
<!-- ========================================================== -->
<section class="cta-band" style="background: var(--ink); color: #fff;">
  <div class="container" style="text-align:center;">
    <h2 style="color:#fff;">Ready to start your <span style="color:var(--accent);font-style:italic;font-weight:300;">{name}</span> project?</h2>
    <p style="color:rgba(255,255,255,0.7);">Fixed fees from &pound;840. MCIAT chartered. 98% first-time approval.</p>
    <div style="display: flex; gap: 12px; justify-content: center; flex-wrap: wrap;">
      <a href="../../../quote.html?location={slug}" class="btn btn-primary btn-lg" style="background:var(--accent);color:#fff;">Get a free {name} quote &rarr;</a>
      <a href="../../../services.html" class="btn btn-outline btn-lg" style="border-color:rgba(255,255,255,0.3);color:#fff;">All services</a>
    </div>
  </div>
</section>

<!-- ========================================================== -->
<!-- 12. Dark footer with .footer-seo                           -->
<!-- ========================================================== -->
<footer class="footer">
  <div class="container">
    <div class="footer-seo">
      <div>
        <h5>Services</h5>
        <ul>
          <li><a href="/services/planning-drawings.html">Planning permission drawings</a></li>
          <li><a href="/services/building-regulations.html">Building regulations drawings</a></li>
          <li><a href="/services/loft-conversions.html">Loft conversion drawings</a></li>
          <li><a href="/services/house-extensions.html">House extension plans</a></li>
          <li><a href="/services/mansard-roof.html">Mansard roof extensions</a></li>
        </ul>
      </div>
      <div>
        <h5>Surrey &amp; Kent</h5>
        <ul>
          <li><a href="/areas/commuter/guildford/">Architectural drawings Guildford</a></li>
          <li><a href="/areas/commuter/woking/">Architectural drawings Woking</a></li>
          <li><a href="/areas/commuter/epsom/">Architectural drawings Epsom</a></li>
          <li><a href="/areas/commuter/sevenoaks/">Architectural drawings Sevenoaks</a></li>
          <li><a href="/areas/commuter/tunbridge-wells/">Architectural drawings Tunbridge Wells</a></li>
        </ul>
      </div>
      <div>
        <h5>Herts &amp; Essex</h5>
        <ul>
          <li><a href="/areas/commuter/watford/">Architectural drawings Watford</a></li>
          <li><a href="/areas/commuter/st-albans/">Architectural drawings St Albans</a></li>
          <li><a href="/areas/commuter/chelmsford/">Architectural drawings Chelmsford</a></li>
          <li><a href="/areas/commuter/brentwood/">Architectural drawings Brentwood</a></li>
          <li><a href="/areas/commuter/harlow/">Architectural drawings Harlow</a></li>
        </ul>
      </div>
      <div>
        <h5>Bucks, Berks &amp; Oxon</h5>
        <ul>
          <li><a href="/areas/commuter/high-wycombe/">Architectural drawings High Wycombe</a></li>
          <li><a href="/areas/commuter/amersham/">Architectural drawings Amersham</a></li>
          <li><a href="/areas/commuter/beaconsfield/">Architectural drawings Beaconsfield</a></li>
          <li><a href="/areas/commuter/windsor/">Architectural drawings Windsor</a></li>
          <li><a href="/areas/commuter/oxford/">Architectural drawings Oxford</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom" style="border-top: 1px solid rgba(255,255,255,0.1); padding-top: 24px; margin-top: 24px; display:flex;flex-wrap:wrap;gap:12px;justify-content:space-between;">
      <span>&copy; 2026 Architectural Drawings Ltd &middot; 86\u201390 Paul Street, London EC2A 4NE</span>
      <span><a href="/">Home</a> &middot; <a href="/services.html">Services</a> &middot; <a href="/pricing.html">Pricing</a> &middot; <a href="/areas/commuter/">Commuter belt</a></span>
    </div>
  </div>
</footer>

<script>
(() => {{
  'use strict';
  const reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && reveals.length) {{
    const io = new IntersectionObserver((entries) => {{
      entries.forEach((entry) => {{
        if (entry.isIntersecting) {{ entry.target.classList.add('in'); io.unobserve(entry.target); }}
      }});
    }}, {{ threshold: 0.1, rootMargin: '0px 0px -60px 0px' }});
    reveals.forEach((el) => io.observe(el));
  }} else {{
    reveals.forEach((el) => el.classList.add('in'));
  }}
  const nav = document.getElementById('nav');
  if (nav) {{
    const onScroll = () => {{ nav.classList.toggle('scrolled', window.scrollY > 12); }};
    onScroll();
    window.addEventListener('scroll', onScroll, {{ passive: true }});
  }}
  document.querySelectorAll('.faq-item').forEach((item) => {{
    item.addEventListener('toggle', () => {{ item.classList.toggle('open', item.open); }});
  }});
}})();
</script>

<!-- WhatsApp + Phone FABs -->
<div style="position:fixed;right:1.25rem;bottom:1.25rem;display:flex;flex-direction:column;gap:0.75rem;z-index:90;">
  <a href="tel:+442079460000" style="width:52px;height:52px;border-radius:50%;background:var(--accent);color:#fff;display:grid;place-items:center;box-shadow:0 14px 30px -8px rgba(14,17,22,0.25);" aria-label="Call us">
    <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.81.36 1.59.7 2.32a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.73.34 1.51.57 2.32.7A2 2 0 0 1 22 16.92z"/></svg>
  </a>
  <a href="https://wa.me/442079460000?text=Hi%2C%20I%27d%20like%20to%20enquire%20about%20architectural%20drawings%20for%20my%20{name.replace(' ', '%20')}%20project." target="_blank" rel="noopener" style="width:52px;height:52px;border-radius:50%;background:#25D366;color:#fff;display:grid;place-items:center;box-shadow:0 14px 30px -8px rgba(14,17,22,0.25);" aria-label="WhatsApp">
    <svg viewBox="0 0 24 24" width="24" height="24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51a3.04 3.04 0 0 0-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413z"/></svg>
  </a>
</div>

</body>
</html>"""
    return html


# ---------------------------------------------------------------------------
# Master index page
# ---------------------------------------------------------------------------
def generate_index():
    # Group towns by county for presentation
    by_county = {}
    for slug, t in TOWNS.items():
        by_county.setdefault(t["county"], []).append((slug, t))

    county_sections = []
    for county in sorted(by_county.keys()):
        cards = []
        for slug, t in by_county[county]:
            cards.append(
                f'<a href="./{slug}/" style="display:block;padding:24px 26px;background:var(--surface);border:1px solid var(--line);border-radius:var(--r-lg);text-decoration:none;transition:all 0.3s var(--ease);">'
                f'<div style="font-family:var(--font-display);font-size:1.35rem;font-variation-settings:\'opsz\' 60;color:var(--ink);margin-bottom:6px;">{t["name"]}</div>'
                f'<div style="color:var(--ink-soft);font-size:0.88rem;margin-bottom:12px;">{t["distance_from_london"]} \u00b7 {t["travel_time"]}</div>'
                f'<div style="color:var(--accent-deep);font-size:0.84rem;font-weight:600;">View services &rarr;</div>'
                f'</a>'
            )
        county_sections.append(
            f'<div style="margin-bottom: 48px;">'
            f'<h2 style="font-family:var(--font-display);font-size:clamp(1.6rem,3vw,2.2rem);margin-bottom:20px;">{county} <span style="color:var(--ink-soft);font-weight:300;font-size:0.7em;">({len(by_county[county])} towns)</span></h2>'
            f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px;">'
            f'{chr(10).join(cards)}'
            f'</div></div>'
        )

    county_html = "\n".join(county_sections)

    title = "Architectural Drawings Across the M25 Commuter Belt | AD London"
    meta_desc = "MCIAT chartered architectural drawings across the M25 commuter belt \u2014 30 commuter towns in Surrey, Kent, Herts, Essex, Bucks, Berks, Beds and Oxon. Fixed fees from \u00a3840."
    canonical = "https://www.architecturaldrawings.uk/areas/commuter/"

    # Hero SVG for index
    hero_svg = gradient_hero("Commuter Belt", "30 towns around London")

    html = f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8" />
<link rel="alternate" hreflang="en-GB" href="https://www.architecturaldrawings.uk/" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{title}</title>
<meta name="description" content="{meta_desc}" />
<link rel="author" href="/team/" />
<link rel="canonical" href="{canonical}" />

<meta property="og:type" content="website" />
<meta property="og:url" content="{canonical}" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{meta_desc}" />
<meta property="og:locale" content="en_GB" />
<meta name="twitter:card" content="summary_large_image" />

<!-- BreadcrumbList schema -->
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{ "@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.architecturaldrawings.uk/" }},
    {{ "@type": "ListItem", "position": 2, "name": "Areas we cover", "item": "https://www.architecturaldrawings.uk/areas/" }},
    {{ "@type": "ListItem", "position": 3, "name": "Commuter belt", "item": "{canonical}" }}
  ]
}}
</script>

<!-- ItemList schema -->
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "ItemList",
  "name": "M25 commuter belt towns covered",
  "numberOfItems": {len(TOWNS)},
  "itemListElement": [
{','.join(f'    {{"@type":"ListItem","position":{i+1},"name":"{t["name"]}","url":"https://www.architecturaldrawings.uk/areas/commuter/{s}/"}}' for i, (s, t) in enumerate(TOWNS.items()))}
  ]
}}
</script>

<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,200..900,0..100;1,9..144,200..900,0..100&family=Manrope:wght@300;400;500;600;700;800&display=swap" media="print" onload="this.media='all'" />
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,200..900,0..100;1,9..144,200..900,0..100&family=Manrope:wght@300;400;500;600;700;800&display=swap" /></noscript>
<link rel="stylesheet" href="/assets/css/style.css" />

<style>
{css_escaped}

.commuter-hero {{
  position: relative;
  border-radius: var(--r-xl);
  overflow: hidden;
  aspect-ratio: 25 / 10;
  margin-bottom: 40px;
}}
.commuter-hero > svg {{ position: absolute; inset: 0; width: 100%; height: 100%; }}
.breadcrumbs {{ font-size: 0.84rem; color: var(--ink-soft); margin-bottom: 24px; }}
.breadcrumbs a {{ color: var(--ink-soft); text-decoration: none; font-weight: 500; }}
.breadcrumbs a:hover {{ color: var(--accent-deep); }}
.breadcrumbs span {{ margin: 0 6px; opacity: 0.5; }}

.footer {{ background: var(--ink); color: rgba(250,250,247,0.6); }}
.footer .logo {{ color: var(--bg); }}
.footer .logo-mark {{ background: var(--bg); color: var(--ink); }}
.footer-col p, .footer-col h5 {{ color: rgba(250,250,247,0.5); }}
.footer-col a {{ color: rgba(250,250,247,0.6); }}
.footer-col a:hover {{ color: var(--accent); }}

@keyframes __ad_safety_in {{ to {{ opacity: 1; transform: none; }} }}
.reveal {{ animation: __ad_safety_in 0.01s linear 1.5s forwards; }}
.reveal.in {{ animation: none; opacity: 1; transform: none; }}
</style>
</head>
<body>

<header class="nav" id="nav">
  <div class="container nav-inner">
    <a href="../../" class="logo"><span class="logo-mark">A</span><span>Architectural<span style="color:var(--accent);font-style:italic;font-weight:400;"> Drawings</span></span></a>
    <nav><ul class="nav-links">
      <li><a href="../../services.html">Services</a></li>
      <li><a href="../../pricing.html">Pricing</a></li>
      <li><a href="../../index.html#process">Process</a></li>
      <li><a href="../../about.html">About</a></li>
    </ul></nav>
    <div class="nav-cta">
      <a href="../../portal/login.html" class="btn btn-ghost btn-sm">Sign in</a>
      <a href="../../quote.html" class="btn btn-primary btn-sm">Free quote</a>
    </div>
  </div>
</header>

<section class="hero">
  <div class="container" style="max-width: 1100px;">
    <nav class="breadcrumbs">
      <a href="../../">Home</a><span>/</span><a href="../">Areas</a><span>/</span>Commuter belt
    </nav>
    <h1 style="margin: 0 0 20px; font-size: clamp(2.4rem, 5.5vw, 4.6rem);">Architectural Drawings Across the <em style="color: var(--accent); font-weight: 300;">M25 Commuter Belt</em></h1>
    <p style="max-width: 760px; font-size: 1.15rem; color: var(--ink-soft); line-height: 1.6; margin-bottom: 32px;">
      MCIAT chartered architectural technology across {len(TOWNS)} commuter towns within our 50-mile service radius from London.
      Planning permission, building regulations, loft conversions, extensions and mansard roofs \u2014 fixed fees from &pound;840.
    </p>
    <div style="display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 40px;">
      <a href="../../quote.html" class="btn btn-primary btn-lg">Get a free quote &rarr;</a>
      <a href="../" class="btn btn-outline btn-lg">All London boroughs</a>
    </div>
    <div class="commuter-hero reveal">
      {hero_svg}
    </div>
  </div>
</section>

<section style="padding-top: 24px;">
  <div class="container" style="max-width: 1100px;">
    <div style="max-width: 760px; margin-bottom: 48px;">
      <span class="eyebrow">Coverage</span>
      <h2 style="font-size: clamp(2rem, 4vw, 3rem); margin: 12px 0 16px;">The full M25 commuter belt</h2>
      <p style="color: var(--ink-soft); font-size: 1.05rem; line-height: 1.6;">
        We cover {len(TOWNS)} commuter towns across Surrey, Kent, Hertfordshire, Essex, Buckinghamshire, Berkshire, Bedfordshire and Oxfordshire. Every project is delivered by MCIAT chartered architectural technologists from our central London office, with travel time included in the fixed fee.
      </p>
    </div>
    {county_html}
  </div>
</section>

<section class="cta-band" style="background: var(--ink); color: #fff;">
  <div class="container" style="text-align:center;">
    <h2 style="color:#fff;">Not sure if we cover your <span style="color:var(--accent);font-style:italic;font-weight:300;">town?</span></h2>
    <p style="color:rgba(255,255,255,0.7);">We take projects anywhere within a 50-mile radius of central London. If your town isn't listed above, drop us a line \u2014 we probably still cover it.</p>
    <div style="display: flex; gap: 12px; justify-content: center; flex-wrap: wrap;">
      <a href="../../quote.html" class="btn btn-primary btn-lg" style="background:var(--accent);color:#fff;">Check your postcode</a>
      <a href="tel:+442079460000" class="btn btn-outline btn-lg" style="border-color:rgba(255,255,255,0.3);color:#fff;">020 7946 0000</a>
    </div>
  </div>
</section>

<footer class="footer">
  <div class="container">
    <div class="footer-seo">
      <div>
        <h5>Services</h5>
        <ul>
          <li><a href="/services/planning-drawings.html">Planning permission drawings</a></li>
          <li><a href="/services/building-regulations.html">Building regulations drawings</a></li>
          <li><a href="/services/loft-conversions.html">Loft conversion drawings</a></li>
          <li><a href="/services/house-extensions.html">House extension plans</a></li>
          <li><a href="/services/mansard-roof.html">Mansard roof extensions</a></li>
        </ul>
      </div>
      <div>
        <h5>Surrey &amp; Kent</h5>
        <ul>
          <li><a href="/areas/commuter/guildford/">Guildford</a></li>
          <li><a href="/areas/commuter/woking/">Woking</a></li>
          <li><a href="/areas/commuter/sevenoaks/">Sevenoaks</a></li>
          <li><a href="/areas/commuter/tunbridge-wells/">Tunbridge Wells</a></li>
          <li><a href="/areas/commuter/dartford/">Dartford</a></li>
        </ul>
      </div>
      <div>
        <h5>Herts &amp; Essex</h5>
        <ul>
          <li><a href="/areas/commuter/watford/">Watford</a></li>
          <li><a href="/areas/commuter/st-albans/">St Albans</a></li>
          <li><a href="/areas/commuter/chelmsford/">Chelmsford</a></li>
          <li><a href="/areas/commuter/brentwood/">Brentwood</a></li>
          <li><a href="/areas/commuter/harlow/">Harlow</a></li>
        </ul>
      </div>
      <div>
        <h5>Bucks, Berks &amp; Oxon</h5>
        <ul>
          <li><a href="/areas/commuter/high-wycombe/">High Wycombe</a></li>
          <li><a href="/areas/commuter/amersham/">Amersham</a></li>
          <li><a href="/areas/commuter/beaconsfield/">Beaconsfield</a></li>
          <li><a href="/areas/commuter/windsor/">Windsor</a></li>
          <li><a href="/areas/commuter/oxford/">Oxford</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom" style="border-top: 1px solid rgba(255,255,255,0.1); padding-top: 24px; margin-top: 24px; display:flex;flex-wrap:wrap;gap:12px;justify-content:space-between;">
      <span>&copy; 2026 Architectural Drawings Ltd &middot; 86\u201390 Paul Street, London EC2A 4NE</span>
      <span><a href="/">Home</a> &middot; <a href="/services.html">Services</a> &middot; <a href="/pricing.html">Pricing</a> &middot; <a href="/areas/">Areas</a></span>
    </div>
  </div>
</footer>

<script>
(() => {{
  'use strict';
  const reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && reveals.length) {{
    const io = new IntersectionObserver((entries) => {{
      entries.forEach((entry) => {{
        if (entry.isIntersecting) {{ entry.target.classList.add('in'); io.unobserve(entry.target); }}
      }});
    }}, {{ threshold: 0.1, rootMargin: '0px 0px -60px 0px' }});
    reveals.forEach((el) => io.observe(el));
  }} else {{
    reveals.forEach((el) => el.classList.add('in'));
  }}
  const nav = document.getElementById('nav');
  if (nav) {{
    const onScroll = () => {{ nav.classList.toggle('scrolled', window.scrollY > 12); }};
    onScroll();
    window.addEventListener('scroll', onScroll, {{ passive: true }});
  }}
}})();
</script>

<!-- WhatsApp + Phone FABs -->
<div style="position:fixed;right:1.25rem;bottom:1.25rem;display:flex;flex-direction:column;gap:0.75rem;z-index:90;">
  <a href="tel:+442079460000" style="width:52px;height:52px;border-radius:50%;background:var(--accent);color:#fff;display:grid;place-items:center;box-shadow:0 14px 30px -8px rgba(14,17,22,0.25);" aria-label="Call us">
    <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.81.36 1.59.7 2.32a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.73.34 1.51.57 2.32.7A2 2 0 0 1 22 16.92z"/></svg>
  </a>
  <a href="https://wa.me/442079460000?text=Hi%2C%20I%27d%20like%20to%20enquire%20about%20architectural%20drawings%20in%20the%20M25%20commuter%20belt." target="_blank" rel="noopener" style="width:52px;height:52px;border-radius:50%;background:#25D366;color:#fff;display:grid;place-items:center;box-shadow:0 14px 30px -8px rgba(14,17,22,0.25);" aria-label="WhatsApp">
    <svg viewBox="0 0 24 24" width="24" height="24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51a3.04 3.04 0 0 0-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413z"/></svg>
  </a>
</div>

</body>
</html>"""
    return html


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    count = 0

    # Master index
    index_path = OUT_DIR / "index.html"
    index_path.write_text(generate_index(), encoding="utf-8")
    count += 1
    print(f"  Generated: areas/commuter/index.html")

    # One page per town
    for slug, t in TOWNS.items():
        town_dir = OUT_DIR / slug
        town_dir.mkdir(parents=True, exist_ok=True)
        html = generate_page(slug, t)
        out_path = town_dir / "index.html"
        out_path.write_text(html, encoding="utf-8")
        count += 1
        print(f"  Generated: areas/commuter/{slug}/index.html")

    print(f"\nDone. {count} commuter-belt pages generated in areas/commuter/")


if __name__ == "__main__":
    main()
