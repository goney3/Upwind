"""
data/questions.py - Comprehensive 90-Question Bank for FAA FAR Part 103 & Ultralight Safety.
Covers: Regulations, Airspace, 2-Stroke/4-Stroke Mechanics, Aerodynamics, Weather, and Emergencies.
"""

def get_question_pool():
    return [
        # =========================================================================
        # SECTION 1: FAR PART 103 REGULATIONS & FAA AC 103-7 (Questions 1 - 20)
        # =========================================================================
        {
            "question_text": "What is the maximum empty weight for a powered ultralight vehicle under FAR Part 103?",
            "options": ["254 pounds", "155 pounds", "300 pounds", "500 pounds"],
            "correct_answer": "254 pounds",
            "explanation": "FAR Part 103.1(e)(1) limits powered ultralights to less than 254 pounds empty weight, excluding floats and safety devices."
        },
        {
            "question_text": "Under FAA AC 103-7, how much weight deduction is granted for an installed deployable ballistic parachute?",
            "options": ["Up to 24 pounds", "Up to 12 pounds", "Up to 50 pounds", "No allowance is granted"],
            "correct_answer": "Up to 24 pounds",
            "explanation": "AC 103-7 allows up to a 24-pound empty weight deduction for an installed ballistic parachute recovery system (BRS)."
        },
        {
            "question_text": "Under AC 103-7, what is the maximum weight allowance permitted for amphibious floats installed on an ultralight?",
            "options": ["60 pounds total", "30 pounds total", "100 pounds total", "The actual weight of the floats"],
            "correct_answer": "60 pounds total",
            "explanation": "AC 103-7 allows up to 60 pounds total weight allowance for amphibious floats to account for wheels and retraction gear."
        },
        {
            "question_text": "Under AC 103-7, what is the weight allowance for non-amphibious (pure water) floats?",
            "options": ["30 pounds per float", "60 pounds per float", "15 pounds total", "No allowance"],
            "correct_answer": "30 pounds per float",
            "explanation": "AC 103-7 authorizes a weight credit of up to 30 pounds per float for non-amphibious floats (up to 60 pounds total for a dual-float setup)."
        },
        {
            "question_text": "What is the maximum fuel capacity for a powered ultralight under Part 103?",
            "options": ["5 U.S. gallons", "10 U.S. gallons", "3 U.S. gallons", "There is no limit"],
            "correct_answer": "5 U.S. gallons",
            "explanation": "FAR Part 103.1(e)(2) strictly limits fuel capacity to a maximum of 5 U.S. gallons."
        },
        {
            "question_text": "An ultralight has an 8-gallon fuel tank installed, but the pilot only fills it with 4 gallons. Is this compliant?",
            "options": [
                "No, the tank capacity itself cannot exceed 5 U.S. gallons",
                "Yes, because only 4 gallons are carried",
                "Yes, if an FAA waiver is obtained",
                "Only if flown in Class G airspace"
            ],
            "correct_answer": "No, the tank capacity itself cannot exceed 5 U.S. gallons",
            "explanation": "The regulation applies to the physical volume capacity of the tank. A tank capable of holding more than 5 gallons violates Part 103."
        },
        {
            "question_text": "What is the maximum full-power level flight speed for a legal powered ultralight?",
            "options": ["55 knots (63 mph)", "45 knots (52 mph)", "70 knots (81 mph)", "65 mph"],
            "correct_answer": "55 knots (63 mph)",
            "explanation": "FAR 103.1(e)(3) mandates that the vehicle cannot exceed 55 knots calibrated airspeed at full power in level flight."
        },
        {
            "question_text": "What is the maximum power-off stall speed allowed for an ultralight under Part 103?",
            "options": ["24 knots (28 mph)", "30 knots (35 mph)", "20 knots (23 mph)", "There is no stall speed limit"],
            "correct_answer": "24 knots (28 mph)",
            "explanation": "FAR 103.1(e)(4) requires a power-off stall speed not exceeding 24 knots calibrated airspeed to ensure low-energy forced landings."
        },
        {
            "question_text": "What is the maximum allowable empty weight for an unpowered ultralight vehicle (e.g., hang glider or paraglider)?",
            "options": ["155 pounds", "100 pounds", "200 pounds", "254 pounds"],
            "correct_answer": "155 pounds",
            "explanation": "FAR 103.1(d) specifies that unpowered ultralight vehicles must weigh less than 155 pounds empty weight."
        },
        {
            "question_text": "Are pilot certificates, flight logbook sign-offs, or FAA medical certificates required under Part 103?",
            "options": [
                "No, neither a pilot certificate nor medical certificate is required",
                "Yes, at least a Sport Pilot certificate",
                "Yes, a valid BasicMed or Third-Class Medical",
                "Only when flying near an airport"
            ],
            "correct_answer": "No, neither a pilot certificate nor medical certificate is required",
            "explanation": "FAR 103.7 explicitly exempts ultralight operators from FAA pilot certification and airman medical certification."
        },
        {
            "question_text": "Are aircraft registration markings (N-numbers) required on Part 103 ultralights?",
            "options": [
                "No, ultralights are exempt from registration and display markings",
                "Yes, 3-inch letters on the vertical stabilizer",
                "Only if operating in controlled airspace",
                "Only if equipped with an engine over 25 horsepower"
            ],
            "correct_answer": "No, ultralights are exempt from registration and display markings",
            "explanation": "FAR 103.7(c) states that ultralight vehicles are not required to be registered or to bear markings of any type."
        },
        {
            "question_text": "Can a two-seat ultralight be operated under Part 103 without an FAA exemption?",
            "options": [
                "No, Part 103 vehicles are strictly limited to a single occupant",
                "Yes, for recreational flights with family",
                "Yes, if the aircraft weighs under 496 pounds",
                "Yes, if no compensation is exchanged"
            ],
            "correct_answer": "No, Part 103 vehicles are strictly limited to a single occupant",
            "explanation": "FAR 103.1(a) defines an ultralight vehicle as intended for operation by a single occupant only. Two-place training requires Light-Sport Aircraft (LSA) certification."
        },
        {
            "question_text": "Does adding an electric starter, battery, and avionics count toward the 254-lb empty weight limit?",
            "options": [
                "Yes, only floats and deployable parachutes qualify for weight exclusions",
                "No, navigation and safety equipment are exempt",
                "Only the battery counts toward weight",
                "Starters are exempt if under 15 pounds"
            ],
            "correct_answer": "Yes, only floats and deployable parachutes qualify for weight exclusions",
            "explanation": "Under AC 103-7, only floats and deployable ballistic parachute systems are excluded. All starters, batteries, instruments, and cowlings count toward the 254-lb ceiling."
        },
        {
            "question_text": "Can an ultralight legally fly directly over a congested town, city, or open-air assembly of persons?",
            "options": [
                "No, flight over congested areas of cities, towns, or assemblies is strictly prohibited",
                "Yes, if cruising at least 1,000 feet above ground",
                "Yes, if maintaining glide path to a city park",
                "Only during daylight hours"
            ],
            "correct_answer": "No, flight over congested areas of cities, towns, or assemblies is strictly prohibited",
            "explanation": "FAR 103.15 strictly bans operations over any congested area of a city, town, settlement, or open-air assembly of persons."
        },
        {
            "question_text": "Can a Part 103 ultralight be hired out to inspect ranch fence lines, photograph real estate, or drop advertisements?",
            "options": [
                "No, commercial operations of any kind are strictly prohibited",
                "Yes, if the pilot holds an FAA Commercial Pilot license",
                "Yes, if flown below 500 feet AGL",
                "Only if the total payment is under $500"
            ],
            "correct_answer": "No, commercial operations of any kind are strictly prohibited",
            "explanation": "FAR 103.1(b) mandates that ultralights are used exclusively for recreation or sport purposes only. Any commercial operation for compensation or hire is illegal."
        },
        {
            "question_text": "When are ultralight vehicles permitted to operate under FAR 103.11?",
            "options": [
                "Between sunrise and sunset (daylight hours)",
                "Day or night with a landing light",
                "Only on weekends and federal holidays",
                "24 hours a day in Class G airspace"
            ],
            "correct_answer": "Between sunrise and sunset (daylight hours)",
            "explanation": "FAR 103.11(a) restricts operations to daylight hours (sunrise to sunset), with a specific provision for civil twilight."
        },
        {
            "question_text": "Under what condition may an ultralight operate during civil twilight (30 min before sunrise / 30 min after sunset)?",
            "options": [
                "If equipped with an operating anti-collision light visible for at least 3 statute miles, operating strictly in Class G airspace",
                "With a handheld aviation radio and transponder",
                "If within 1 mile of an ultralight flightpark",
                "Twilight operations are strictly prohibited under all circumstances"
            ],
            "correct_answer": "If equipped with an operating anti-collision light visible for at least 3 statute miles, operating strictly in Class G airspace",
            "explanation": "FAR 103.11(b) permits twilight flight only in Class G airspace when equipped with an operating anti-collision light visible for at least 3 statute miles."
        },
        {
            "question_text": "An ultralight is converging with a general aviation Cessna 172. Who is legally required to yield the right-of-way?",
            "options": [
                "The ultralight must yield to the Cessna 172",
                "The Cessna 172 yields to the slower ultralight",
                "Whoever is on the right has right-of-way",
                "Whoever is higher yields"
            ],
            "correct_answer": "The ultralight must yield to the Cessna 172",
            "explanation": "FAR 103.13(a) explicitly states that ultralight vehicles shall yield the right-of-way to all other aircraft."
        },
        {
            "question_text": "A powered ultralight and an unpowered hang glider are converging at the same altitude. Who must yield?",
            "options": [
                "The powered ultralight must yield to the unpowered ultralight",
                "The unpowered hang glider yields",
                "Both aircraft must turn left",
                "Whoever is flying faster yields"
            ],
            "correct_answer": "The powered ultralight must yield to the unpowered ultralight",
            "explanation": "FAR 103.13(c) requires powered ultralights to yield right-of-way to unpowered ultralights."
        },
        {
            "question_text": "Can objects be dropped from an ultralight in flight under FAR 103.9?",
            "options": [
                "Only if the drop does not create a hazard to persons or property on the ground",
                "No, dropping any object is strictly prohibited under federal law",
                "Yes, anywhere as long as an altitude of 500 feet is maintained",
                "Only with prior FAA FSDO written authorization"
            ],
            "correct_answer": "Only if the drop does not create a hazard to persons or property on the ground",
            "explanation": "FAR 103.9(b) allows dropping objects only if operations are conducted in a manner that does not create a hazard to persons or property (e.g., wind streamers over open fields)."
        },

        # =========================================================================
        # SECTION 2: INDUSTRIAL 4-STROKES & HALF-VW CONVERSIONS (Questions 21 - 38)
        # =========================================================================
        {
            "question_text": "Why do direct-drive industrial engines (such as a Predator 420cc or 670cc) typically swing a smaller 40\"–44\" propeller rather than a 54\"–60\" prop?",
            "options": [
                "Because at direct-drive engine speeds (3,600 RPM), a 42\" prop tip speed is Mach 0.59 (subsonic), whereas a 60\" prop tip speed would exceed Mach 0.84 (transonic drag rise and flutter)",
                "Because large propellers are prohibited on 4-stroke engines",
                "Because industrial engines only turn counter-clockwise",
                "Because 4-stroke engines require less thrust to fly"
            ],
            "correct_answer": "Because at direct-drive engine speeds (3,600 RPM), a 42\" prop tip speed is Mach 0.59 (subsonic), whereas a 60\" prop tip speed would exceed Mach 0.84 (transonic drag rise and flutter)",
            "explanation": "Propeller tip speed is directly proportional to diameter and RPM. At 3,600 RPM, a 42\" prop maintains safe sub-transonic tip speeds (~660 ft/s, Mach 0.59). A 60\" prop at that RPM would spin at 942 ft/s (Mach 0.84), causing shock flutter, noise, and power loss."
        },
        {
            "question_text": "What happens if you bolt a large 60\" propeller directly to the crankshaft of a 22-hp Predator engine without a reduction drive?",
            "options": [
                "The excessive aerodynamic drag will lug the engine down to ~2,000 RPM where it makes only 8 hp, preventing takeoff power",
                "The engine will instantly over-rev past 6,000 RPM",
                "The oil pressure will spike to 120 PSI",
                "The carburetor will freeze instantly"
            ],
            "correct_answer": "The excessive aerodynamic drag will lug the engine down to ~2,000 RPM where it makes only 8 hp, preventing takeoff power",
            "explanation": "A direct-drive industrial engine relies on spinning at 3,400–3,800 RPM to develop its rated horsepower. Over-propping lugs the engine down below its power curve."
        },
        {
            "question_text": "What cold valve lash clearance is typically specified for intake and exhaust on a solid-lifter Half-VW conversion engine?",
            "options": ["0.006 inches", "0.020 inches", "0.001 inches", "0.030 inches"],
            "correct_answer": "0.006 inches",
            "explanation": "Standard solid-lifter Half-VW engines specify 0.006 inches cold valve lash. Inadequate lash causes burnt valves when valve stems expand during full-throttle climb heat."
        },
        {
            "question_text": "What is the consequence of setting valve lash too tight (e.g. 0.001\" instead of 0.006\") on an air-cooled 4-stroke aero conversion?",
            "options": [
                "Thermal expansion during climb prevents valves from fully seating, causing cylinder compression loss and burnt exhaust valves",
                "Excessive valve clatter and rocker arm damage",
                "The oil pump will lose pressure",
                "The spark plugs will fowl with soot"
            ],
            "correct_answer": "Thermal expansion during climb prevents valves from fully seating, causing cylinder compression loss and burnt exhaust valves",
            "explanation": "As the engine reaches operating temperature, valve stems expand. Without proper cold lash, valves stay slightly cracked open, allowing burning exhaust gases to melt the valve face."
        },
        {
            "question_text": "What is the minimum safe oil temperature before full-power takeoff in a 4-stroke Half-VW conversion engine?",
            "options": ["160°F (71°C)", "100°F (38°C)", "230°F (110°C)", "4-stroke engines do not require warmup"],
            "correct_answer": "160°F (71°C)",
            "explanation": "A minimum oil temp of 160°F ensures proper viscosity and allows the crankcase to vaporize condensation and unburned fuel contaminants."
        },
        {
            "question_text": "What is the maximum redline oil temperature for an air-cooled 4-stroke engine using conventional aviation mineral or multi-grade oil?",
            "options": ["220°F to 230°F (104°C to 110°C)", "150°F (65°C)", "350°F (177°C)", "400°F (204°C)"],
            "correct_answer": "220°F to 230°F (104°C to 110°C)",
            "explanation": "Oil temperatures exceeding 220°F–230°F cause thermal breakdown of viscosity, thinning the hydrodynamic oil film and risking rod bearing seizure."
        },
        {
            "question_text": "Why must an industrial 4-stroke V-Twin (e.g., Briggs Vanguard or Kohler Command) have its stock mechanical governor bypassed or modified for aviation?",
            "options": [
                "Stock governors limit RPM to 3,600, preventing maximum climb power and causing dangerous throttle hunting/surging in flight",
                "Industrial governors cause immediate spark plug failure",
                "Federal law strictly bans governors on all aircraft",
                "Governors prevent oil from reaching the overhead valves"
            ],
            "correct_answer": "Stock governors limit RPM to 3,600, preventing maximum climb power and causing dangerous throttle hunting/surging in flight",
            "explanation": "Industrial governors are designed for constant-speed mowers. In flight, they fight the pilot's throttle commands and prevent the engine from reaching climb RPM."
        },
        {
            "question_text": "What mechanical upgrade is mandatory on an industrial V-Twin if the governor is removed and the engine is run up to 4,200 RPM?",
            "options": [
                "Upgraded heavy-duty valve springs to prevent valve float",
                "A second carburetor",
                "Ceramic piston rings",
                "A dry-sump oil pump"
            ],
            "correct_answer": "Upgraded heavy-duty valve springs to prevent valve float",
            "explanation": "Stock industrial valve springs are weak and cannot seat valves quickly past 3,800 RPM. Heavy-duty springs prevent valve float and piston-valve collisions."
        },
        {
            "question_text": "Why is full-pressure lubrication with a spin-on filter required when using an industrial engine on an ultralight?",
            "options": [
                "Splash-lubricated engines suffer oil starvation in steep climb attitudes, destroying connecting rods within minutes",
                "Pressure lubrication is required to cool the propeller",
                "Splash lubrication only works with aviation 100LL fuel",
                "Pressure lubrication eliminates the need for an oil sump"
            ],
            "correct_answer": "Splash-lubricated engines suffer oil starvation in steep climb attitudes, destroying connecting rods within minutes",
            "explanation": "Splash dippers rely on a level oil pool. In a 12° climb attitude, oil flows to the rear of the case, uncovering the dippers and causing rod starvation."
        },
        {
            "question_text": "Why do 90° V-Twin 4-stroke engines require flexible drive couplings or centrifugal clutches when driving a reduction unit?",
            "options": [
                "Because their uneven firing intervals produce severe torsional vibration pulses that can snap reduction belts and fatigue prop hubs",
                "To reverse propeller rotation",
                "To prevent the propeller from freewheeling on landing",
                "Because V-twins have no flywheels"
            ],
            "correct_answer": "Because their uneven firing intervals produce severe torsional vibration pulses that can snap reduction belts and fatigue prop hubs",
            "explanation": "A 90° V-Twin fires at 270° and 450° intervals. These uneven torque pulses cause torsional resonance that will destroy belts and fatigue prop hubs without damping."
        },
        {
            "question_text": "Why are tight, sealed aluminum cooling baffles critical on an air-cooled Half-VW engine?",
            "options": [
                "Because without baffles, ram air takes the path of least resistance over the cylinders, starving the rear cylinder and exhaust valve of cooling airflow",
                "To keep engine oil from spraying the windshield",
                "To keep the engine warm in summer",
                "To reduce aerodynamic drag by 40%"
            ],
            "correct_answer": "Because without baffles, ram air takes the path of least resistance over the cylinders, starving the rear cylinder and exhaust valve of cooling airflow",
            "explanation": "Air-cooled engines require pressure cowls or baffles that force air down between the cylinder fins. Unbaffled engines will overheat the rear cylinder head."
        },
        {
            "question_text": "What is the typical installed weight difference between a 40-hp 2-stroke Rotax 447 and a 4-stroke Half-VW conversion?",
            "options": [
                "A Half-VW is 20 to 30 lbs heavier installed (78–88 lbs vs. 55–60 lbs)",
                "A Half-VW is 20 lbs lighter",
                "They weigh exactly the same",
                "A Half-VW is 100 lbs heavier"
            ],
            "correct_answer": "A Half-VW is 20 to 30 lbs heavier installed (78–88 lbs vs. 55–60 lbs)",
            "explanation": "A 4-stroke Half-VW complete with starter and oil weighs 78–88 lbs. That extra 25+ lbs must be subtracted from the airframe structure to stay under 254 lbs."
        },
        {
            "question_text": "During an extended power-off glide, how does 4-stroke lubrication differ fundamentally from a 2-stroke premix engine?",
            "options": [
                "The 4-stroke crankcase oil pump continues delivering oil to bearings regardless of throttle setting; the 2-stroke loses its oil supply when throttle is closed",
                "Both engines lose all lubrication when the throttle is closed",
                "4-stroke engines lose oil pressure immediately at idle",
                "2-stroke engines generate more oil pressure at idle"
            ],
            "correct_answer": "The 4-stroke crankcase oil pump continues delivering oil to bearings regardless of throttle setting; the 2-stroke loses its oil supply when throttle is closed",
            "explanation": "A 4-stroke holds oil in a separate sump pumped by the crankshaft. In a 2-stroke premix, shutting the throttle shuts off the fuel-oil mix, starving bearings."
        },
        {
            "question_text": "What is the typical fuel burn of a 4-stroke Half-VW cruising at 3,200 RPM compared to a 2-stroke Rotax 503?",
            "options": [
                "Half-VW burns ~2.0 to 2.5 GPH; Rotax 503 burns ~4.0 to 4.5 GPH",
                "Half-VW burns 6.0 GPH; Rotax 503 burns 2.0 GPH",
                "Both engines burn exactly 4.5 GPH",
                "Half-VW burns 0.5 GPH"
            ],
            "correct_answer": "Half-VW burns ~2.0 to 2.5 GPH; Rotax 503 burns ~4.0 to 4.5 GPH",
            "explanation": "4-stroke engines have higher thermal efficiency and do not lose unburned fuel through an exhaust port, burning roughly half the fuel of an equivalent 2-stroke."
        },
        {
            "question_text": "What is the minimum recommended cruise oil pressure for a 4-stroke Half-VW conversion engine?",
            "options": ["25 to 40 PSI", "5 to 10 PSI", "80 to 100 PSI", "Zero PSI is acceptable at cruise"],
            "correct_answer": "25 to 40 PSI",
            "explanation": "A healthy air-cooled VW oil system maintains 25 to 40 PSI at operating temperatures. Less than 20 PSI at cruise indicates impending bearing failure."
        },
        {
            "question_text": "Why is an external oil cooler strongly recommended on 4-stroke industrial and Half-VW conversions?",
            "options": [
                "Because ultralights fly at slow airspeeds (35–50 mph) that provide low cooling airflow while the engine operates at high continuous power",
                "To prevent the oil from freezing at low altitude",
                "Because oil coolers increase fuel octane",
                "To reduce the weight of the engine"
            ],
            "correct_answer": "Because ultralights fly at slow airspeeds (35–50 mph) that provide low cooling airflow while the engine operates at high continuous power",
            "explanation": "Industrial engines rely on cooling fans, but in ultralights they run at 75–85% power at low airspeeds. An external oil cooler prevents oil overheating."
        },
        {
            "question_text": "If oil pressure drops below 15 PSI in a 4-stroke engine during flight, what action must the pilot take?",
            "options": [
                "Reduce power to minimum required for flight, turn immediately toward the nearest landing field, and prepare for an off-field forced landing",
                "Increase throttle to maximum to raise oil pump RPM",
                "Climb to 5,000 feet to cool the engine",
                "Ignore it until the oil temperature gauge rises"
            ],
            "correct_answer": "Reduce power to minimum required for flight, turn immediately toward the nearest landing field, and prepare for an off-field forced landing",
            "explanation": "Loss of oil pressure causes catastrophic bearing failure within 1 to 3 minutes. Head toward a landing site immediately."
        },
        {
            "question_text": "What maintenance step must be performed on an industrial engine conversion after the first 5 to 10 hours of flight testing?",
            "options": [
                "Change engine oil, inspect filter for metal particles, and re-torque cylinder head bolts and propeller bolts",
                "Replace the entire carburetor",
                "Replace the crankshaft",
                "Re-gap spark plugs to 0.080 inches"
            ],
            "correct_answer": "Change engine oil, inspect filter for metal particles, and re-torque cylinder head bolts and propeller bolts",
            "explanation": "Initial running beds in rings and causes thermal settling. Fasteners, heads, and wooden prop hubs loosen and must be re-torqued."
        },

        # =========================================================================
        # SECTION 3: TWO-STROKE ENGINES & FUEL DYNAMICS (Questions 39 - 50)
        # =========================================================================
        {
            "question_text": "Why is closing the throttle completely during a prolonged, steep descent dangerous in a premix two-stroke engine?",
            "options": [
                "The engine loses its lubricating oil supply while spinning at high RPM, risking a lean seizure",
                "The spark plugs will instantly foul with carbon",
                "The fuel tank will over-pressurize",
                "The carburetor float will sink"
            ],
            "correct_answer": "The engine loses its lubricating oil supply while spinning at high RPM, risking a lean seizure",
            "explanation": "In premix two-strokes, fuel carries the lubricating oil. Idling during high-speed descents cuts off oil delivery to bearings spinning at 5,000+ RPM."
        },
        {
            "question_text": "What is a two-stroke 'cold seizure' and how is it prevented?",
            "options": [
                "The aluminum piston expands faster than cold cylinder walls; prevented by thorough pre-takeoff engine warmup",
                "Ice forming in the carburetor venturi; prevented by carb heat",
                "Oil freezing in the fuel lines; prevented by fuel additives",
                "Piston rings seizing due to cold air intake; prevented by leaning mixture"
            ],
            "correct_answer": "The aluminum piston expands faster than cold cylinder walls; prevented by thorough pre-takeoff engine warmup",
            "explanation": "Aluminum pistons expand faster than cylinder liners. Full-throttle takeoffs before reaching operating CHT cause the piston to seize in the bore."
        },
        {
            "question_text": "What minimum Cylinder Head Temperature (CHT) must typically be reached before takeoff on a two-stroke Rotax 447/503?",
            "options": ["250°F (120°C)", "100°F (38°C)", "450°F (232°C)", "350°F (177°C)"],
            "correct_answer": "250°F (120°C)",
            "explanation": "Rotax two-strokes require a minimum of 250°F CHT before applying full takeoff power to ensure cylinder walls expand alongside pistons."
        },
        {
            "question_text": "What happens when automotive gasoline containing ethanol experiences 'phase separation'?",
            "options": [
                "Water bonds with ethanol and precipitates to the bottom as an unburnable, corrosive layer",
                "The fuel octane rating doubles",
                "The fuel evaporates within 20 minutes",
                "The two-stroke oil separates and floats on top"
            ],
            "correct_answer": "Water bonds with ethanol and precipitates to the bottom as an unburnable, corrosive layer",
            "explanation": "Ethanol absorbs ambient water until it separates, dropping to the sump where it starves the engine of combustible fuel and causes sudden stoppage."
        },
        {
            "question_text": "A sudden spike in Exhaust Gas Temperature (EGT) on a two-stroke engine is an immediate warning of:",
            "options": [
                "A dangerously lean fuel-air condition that can melt or hole a piston crown within seconds",
                "An overly rich fuel mixture",
                "An over-filled oil tank",
                "Imminent spark plug fouling"
            ],
            "correct_answer": "A dangerously lean fuel-air condition that can melt or hole a piston crown within seconds",
            "explanation": "High EGT (>1,220°F) signals a lean mixture. Extreme combustion temperatures can melt through an aluminum piston crown in less than 10 seconds."
        },
        {
            "question_text": "What is the typical maximum continuous EGT limit for a Rotax two-stroke engine?",
            "options": ["1,200°F (650°C)", "800°F (426°C)", "1,500°F (815°C)", "1,800°F (982°C)"],
            "correct_answer": "1,200°F (650°C)",
            "explanation": "Rotax specifies a maximum continuous EGT of 1,200°F (650°C). Beyond 1,220°F, aluminum structural strength degrades rapidly."
        },
        {
            "question_text": "What type of oil must be used in a premix aviation two-stroke engine?",
            "options": [
                "High-grade two-stroke oil rated API-TC (formulated for air-cooled engines)",
                "Standard automotive 10W-40 motor oil",
                "TC-W3 marine outboard oil (water-cooled formulation)",
                "Turbine synthetic oil"
            ],
            "correct_answer": "High-grade two-stroke oil rated API-TC (formulated for air-cooled engines)",
            "explanation": "Air-cooled aero engines run much hotter than water-cooled outboards. Marine TC-W3 oil breaks down in air-cooled engines; API-TC is mandatory."
        },
        {
            "question_text": "What is the primary danger of using old, stale fuel mixed with two-stroke oil from the previous season?",
            "options": [
                "Volatile light ends have evaporated, lowering octane and causing detonation, ring sticking, and hard starting",
                "The oil turns into solid wax",
                "Fuel tank capacity increases",
                "The engine will run 400 RPM faster"
            ],
            "correct_answer": "Volatile light ends have evaporated, lowering octane and causing detonation, ring sticking, and hard starting",
            "explanation": "Premixed fuel oxidizes and loses octane over time, leading to detonation and piston crown failure under load."
        },
        {
            "question_text": "How does carburetor icing develop in a two-stroke engine on a warm, humid 75°F day?",
            "options": [
                "Fuel vaporization and the venturi pressure drop reduce air temperature by up to 40°F, freezing ambient humidity onto the throttle slide",
                "High humidity cools the crankcase directly",
                "The exhaust system draws moisture into the carburetor",
                "Two-stroke oil freezes in the fuel jet"
            ],
            "correct_answer": "Fuel vaporization and the venturi pressure drop reduce air temperature by up to 40°F, freezing ambient humidity onto the throttle slide",
            "explanation": "Vaporization absorbs heat, dropping venturi temperature up to 40°F below ambient. Moist 75°F air can cause carburetor icing."
        },
        {
            "question_text": "What is the recommended throttle technique when descending from altitude in a premix two-stroke ultralight?",
            "options": [
                "Maintain partial power or periodically 'blip' the throttle every 5–10 seconds to deliver lubricating oil to the bearings",
                "Pull throttle to dead idle and glide as fast as possible",
                "Shut off the magneto switches",
                "Lean the mixture control"
            ],
            "correct_answer": "Maintain partial power or periodically 'blip' the throttle every 5–10 seconds to deliver lubricating oil to the bearings",
            "explanation": "Blipping the throttle injects fresh fuel-oil mixture into the crankcase, preventing bearing starvation during descents."
        },
        {
            "question_text": "What is a common sign of a leaking crankshaft oil seal in a two-stroke engine?",
            "options": [
                "Unexplained lean running, hard starting, high idle, and elevated EGT on that cylinder due to unmetered air entering",
                "Oil spraying onto the pilot's goggles",
                "Engine refusing to shut off",
                "Cylinder head temperature dropping to zero"
            ],
            "correct_answer": "Unexplained lean running, hard starting, high idle, and elevated EGT on that cylinder due to unmetered air entering",
            "explanation": "Crankshaft seals keep the crankcase airtight. A leaking seal draws in excess air, leaning out the fuel mixture and driving up EGT."
        },
        {
            "question_text": "What is the required carbon-cleaning maintenance interval for exhaust ports and cylinder heads on a typical two-stroke aero engine?",
            "options": ["Every 50 hours of operation", "Every 500 hours", "Only when the engine stops running", "Every 1,000 hours"],
            "correct_answer": "Every 50 hours of operation",
            "explanation": "Rotax recommends decarb maintenance every 50 hours. Carbon accumulation in ring grooves causes stuck rings and piston blow-by."
        },

        # =========================================================================
        # SECTION 4: AERODYNAMICS, LOAD FACTORS & LOW WING LOADING (Questions 51 - 65)
        # =========================================================================
        {
            "question_text": "In a level, coordinated 60-degree banked turn, what load factor (G-load) is imposed on the airframe?",
            "options": ["2.0 G", "1.41 G", "3.0 G", "1.0 G"],
            "correct_answer": "2.0 G",
            "explanation": "Load factor n = 1 / cos(60°) = 1 / 0.5 = 2.0 G. The airframe and pilot feel twice their normal weight."
        },
        {
            "question_text": "How much does the stall speed of your ultralight increase in a 60-degree banked turn?",
            "options": [
                "41% higher (multiplied by 1.41)",
                "Double (100% higher)",
                "Stall speed never changes with bank angle",
                "20% lower"
            ],
            "correct_answer": "41% higher (multiplied by 1.41)",
            "explanation": "Stall speed increases with the square root of load factor (√2.0 ≈ 1.414). A 24-knot stall speed jumps to nearly 34 knots at 60° bank."
        },
        {
            "question_text": "In a 45-degree banked level turn, what is the load factor and approximate stall speed increase?",
            "options": [
                "1.41 G load factor; stall speed increases by approximately 19%",
                "2.0 G load factor; stall speed increases by 50%",
                "1.0 G load factor; no change",
                "3.0 G load factor; stall speed doubles"
            ],
            "correct_answer": "1.41 G load factor; stall speed increases by approximately 19%",
            "explanation": "n = 1 / cos(45°) ≈ 1.41 G. The stall speed multiplier is √1.41 ≈ 1.19 (+19% increase)."
        },
        {
            "question_text": "What aerodynamic condition causes an aircraft to enter an aerodynamic stall?",
            "options": [
                "Exceeding the critical Angle of Attack (AOA), separating airflow from the upper wing surface",
                "Flying at too low an engine RPM",
                "Flying below 500 feet altitude",
                "Flying with the center of gravity too far forward"
            ],
            "correct_answer": "Exceeding the critical Angle of Attack (AOA), separating airflow from the upper wing surface",
            "explanation": "An aerodynamic stall is caused exclusively by exceeding the critical angle of attack. An aircraft can stall at any airspeed or attitude if critical AOA is exceeded."
        },
        {
            "question_text": "What is the primary recovery control input from an impending or full stall?",
            "options": [
                "Immediately lower the nose (relax forward stick) to reduce angle of attack below critical",
                "Pull back firmly on the stick to climb away from the ground",
                "Apply full opposite rudder without touching the stick",
                "Add full throttle while holding the nose up"
            ],
            "correct_answer": "Immediately lower the nose (relax forward stick) to reduce angle of attack below critical",
            "explanation": "The only way to recover from a stall is to reduce the angle of attack below critical by moving the control stick forward."
        },
        {
            "question_text": "What is the deadly hazard of an uncoordinated skidding turn from base to final approach?",
            "options": [
                "The inside wing stalls first, causing a sudden, violent snap-roll and spin at an unrecoverable altitude",
                "The aircraft climbs uncontrollably",
                "The propeller overspeeds",
                "The flaps jam"
            ],
            "correct_answer": "The inside wing stalls first, causing a sudden, violent snap-roll and spin at an unrecoverable altitude",
            "explanation": "Skidding with inside rudder causes the retreating inside wing to stall first, snapping into an unrecoverable low-altitude spin."
        },
        {
            "question_text": "Why are ultralights exceptionally vulnerable to wake turbulence generated by general aviation aircraft?",
            "options": [
                "Ultralights have extremely low wing loading (3–6 lbs/sq ft), allowing wake vortices to easily overwhelm control authority",
                "Ultralights fly faster than wake vortices descend",
                "Ultralights have no rudders",
                "Wake vortices only exist below 500 feet"
            ],
            "correct_answer": "Ultralights have extremely low wing loading (3–6 lbs/sq ft), allowing wake vortices to easily overwhelm control authority",
            "explanation": "Low wing loading and low inertia mean an encounter with the wake vortex of even a light twin or Cessna can invert an ultralight in milliseconds."
        },
        {
            "question_text": "Where does wake turbulence sink and drift relative to the generating aircraft's flight path?",
            "options": [
                "Vortices sink at 400–500 ft/min below the flight path and drift outward with crosswinds near the ground",
                "Vortices rise 500 feet into the air",
                "Vortices remain locked in place forever",
                "Vortices only travel forward"
            ],
            "correct_answer": "Vortices sink at 400–500 ft/min below the flight path and drift outward with crosswinds near the ground",
            "explanation": "Wake vortices generate behind heavy/clean aircraft, sink at several hundred feet per minute, and spread along the runway surface."
        },
        {
            "question_text": "What is the effect of an aft Center of Gravity (CG) on an ultralight vehicle?",
            "options": [
                "Severe longitudinal pitch instability, decreased stick force, and potentially impossible stall/spin recovery",
                "Extremely heavy stick forces and unable to flare",
                "Decreased cruise speed",
                "Automatic stall recovery"
            ],
            "correct_answer": "Severe longitudinal pitch instability, decreased stick force, and potentially impossible stall/spin recovery",
            "explanation": "An aft CG reduces elevator recovery authority, causing pitch instability and potentially fatal unrecoverable stalls or flat spins."
        },
        {
            "question_text": "What is the effect of a forward Center of Gravity (CG) limit exceedance?",
            "options": [
                "Heavy stick forces and insufficient elevator authority to flare for landing, causing hard nose-first touchdown",
                "Violent flat spins",
                "Tail-heavy pitch oscillations",
                "Engine failure on climb"
            ],
            "correct_answer": "Heavy stick forces and insufficient elevator authority to flare for landing, causing hard nose-first touchdown",
            "explanation": "A forward CG creates a heavy nose-down pitching moment, requiring extreme up-elevator that may exhaust control travel during flare."
        },
        {
            "question_text": "Why does pilot body weight cause a much larger percentage shift in CG on an ultralight than on a Cessna 172?",
            "options": [
                "In a 254-lb airframe, a 200-lb pilot represents over 44% of total flight weight",
                "Ultralights have shorter wings",
                "Cessnas use heavier fuel",
                "Ultralights have no center of lift"
            ],
            "correct_answer": "In a 254-lb airframe, a 200-lb pilot represents over 44% of total flight weight",
            "explanation": "Because the empty vehicle weighs so little, occupant weight constitutes almost half the total mass, dominating CG location."
        },
        {
            "question_text": "On a Weight-Shift Control (WSC) trike, what action must the pilot take to pitch up and climb or slow down?",
            "options": [
                "Push the control bar FORWARD (away from the pilot)",
                "Pull the control bar AFT (toward the pilot)",
                "Move the control bar to the left",
                "Press the right foot pedal"
            ],
            "correct_answer": "Push the control bar FORWARD (away from the pilot)",
            "explanation": "Trike controls are reversed relative to 3-axis aircraft: pushing the bar forward moves the pilot's weight aft, raising the wing's angle of attack."
        },
        {
            "question_text": "On a Weight-Shift Control (WSC) trike, pushing the control bar to the RIGHT causes:",
            "options": [
                "A roll and turn to the LEFT",
                "A roll and turn to the RIGHT",
                "A pitch-up maneuver",
                "An immediate stall"
            ],
            "correct_answer": "A roll and turn to the LEFT",
            "explanation": "Pushing the bar right moves the trike's center of gravity right, tilting the wing left and initiating a left bank and turn."
        },
        {
            "question_text": "What dangerous physiological trap occurs when a 3-axis airplane pilot transitions to a weight-shift trike without dual training?",
            "options": [
                "In an emergency panic, ingrained muscle memory causes the pilot to pull back on the bar, which pitches the trike DOWN into a dive",
                "The pilot will forget to use the rudder pedals",
                "The pilot will fly too fast",
                "The pilot cannot reach the throttle"
            ],
            "correct_answer": "In an emergency panic, ingrained muscle memory causes the pilot to pull back on the bar, which pitches the trike DOWN into a dive",
            "explanation": "3-axis instinct is to pull back when ground approaches. On a trike, pulling back dives the aircraft, causing fatal ground collisions."
        },
        {
            "question_text": "Why does a steep spiral dive require immediately leveling the wings BEFORE pulling back on the stick?",
            "options": [
                "Pulling back while steeply banked tightens the spiral, sharply increases G-load, and can exceed structural design limits",
                "Pulling back causes engine stoppage",
                "Leveling wings causes an immediate stall",
                "Rudders lock up in a bank"
            ],
            "correct_answer": "Pulling back while steeply banked tightens the spiral, sharply increases G-load, and can exceed structural design limits",
            "explanation": "Pulling back in a steep bank increases load factor without arresting the descent. Wings must be leveled first before easing out of the dive."
        },

        # =========================================================================
        # SECTION 5: AIRSPACE, SECTIONAL CHARTS & VFR WEATHER (Questions 66 - 78)
        # =========================================================================
        {
            "question_text": "Which classes of airspace require prior ATC authorization before an ultralight may enter under FAR 103.17?",
            "options": [
                "Classes B, C, D, and Class E surface areas designated for an airport",
                "Class G airspace only",
                "Class E airspace above 1,200 feet AGL only",
                "No airspace requires prior authorization"
            ],
            "correct_answer": "Classes B, C, D, and Class E surface areas designated for an airport",
            "explanation": "FAR 103.17 requires prior ATC authorization before entering Class B, C, D, or Class E airport surface areas."
        },
        {
            "question_text": "Can an ultralight vehicle ever enter Class A airspace (18,000' MSL to FL600)?",
            "options": [
                "No, under no circumstances",
                "Yes, with an altitude-reporting transponder",
                "Yes, during daytime VFR conditions",
                "Only with written permission from the FAA Administrator"
            ],
            "correct_answer": "No, under no circumstances",
            "explanation": "Class A is strictly IFR airspace requiring ATC clearances and certified IFR instruments, completely barring ultralights."
        },
        {
            "question_text": "What are the day VFR weather minimums in Class G airspace at or below 1,200 feet AGL?",
            "options": [
                "1 statute mile flight visibility; Clear of clouds",
                "3 statute miles visibility; 500' below, 1,000' above clouds",
                "5 statute miles visibility; 1,000' above and below clouds",
                "3 statute miles visibility; Clear of clouds"
            ],
            "correct_answer": "1 statute mile flight visibility; Clear of clouds",
            "explanation": "In Class G at or below 1,200' AGL, day VFR minimums are 1 statute mile flight visibility and remain clear of clouds."
        },
        {
            "question_text": "What are the VFR weather minimums in Class G airspace above 1,200 feet AGL but below 10,000 feet MSL during daylight?",
            "options": [
                "1 statute mile visibility; 500' below, 1,000' above, 2,000' horizontal from clouds",
                "3 statute miles visibility; 1,000' above, 1,000' below",
                "Clear of clouds with 1/2 mile visibility",
                "5 statute miles visibility; Clear of clouds"
            ],
            "correct_answer": "1 statute mile visibility; 500' below, 1,000' above, 2,000' horizontal from clouds",
            "explanation": "Above 1,200' AGL in Class G during the day, pilots must maintain 1 SM visibility and 500' below, 1,000' above, 2,000' horizontal from clouds."
        },
        {
            "question_text": "On a sectional chart, what does a dashed blue line surrounding an airport depict?",
            "options": ["Class D controlled airspace", "Class B airspace", "Class C airspace", "Class G airspace"],
            "correct_answer": "Class D controlled airspace",
            "explanation": "Dashed blue lines define the lateral limits of Class D controlled airspace around towered airports."
        },
        {
            "question_text": "On a sectional chart, what does a solid magenta line depict?",
            "options": ["Class C controlled airspace", "Class B airspace", "Class D airspace", "Prohibited airspace"],
            "correct_answer": "Class C controlled airspace",
            "explanation": "Solid magenta lines depict the lateral boundaries and shelf altitudes of Class C controlled airspace."
        },
        {
            "question_text": "On a sectional chart, what does a solid blue line depict?",
            "options": ["Class B controlled airspace", "Class C airspace", "Class D airspace", "Military Operations Area (MOA)"],
            "correct_answer": "Class B controlled airspace",
            "explanation": "Solid blue concentric circles indicate the multiple tiers and shelves of Class B airspace around major hubs."
        },
        {
            "question_text": "What does a dashed magenta line surrounding an airport indicate on a sectional chart?",
            "options": [
                "Class E airspace extending down to the surface (prior ATC authorization required for ultralights)",
                "Class G airspace only",
                "A parachute jumping zone",
                "An abandoned military airfield"
            ],
            "correct_answer": "Class E airspace extending down to the surface (prior ATC authorization required for ultralights)",
            "explanation": "Dashed magenta lines depict Class E surface areas. Under FAR 103.17, ultralights cannot enter without prior ATC authorization."
        },
        {
            "question_text": "What does a faded magenta vignette band indicate on a sectional chart?",
            "options": [
                "Class E airspace floor begins at 700 feet AGL (Class G extends from surface to 700' AGL inside the shaded area)",
                "Class E airspace begins at 10,000 feet MSL",
                "Ultralights are prohibited inside the shading",
                "A military bombing corridor"
            ],
            "correct_answer": "Class E airspace floor begins at 700 feet AGL (Class G extends from surface to 700' AGL inside the shaded area)",
            "explanation": "The magenta vignette indicates that controlled Class E airspace transitions down to 700 feet AGL. Below 700' is uncontrolled Class G."
        },
        {
            "question_text": "What is the Maximum Elevation Figure (MEF) shown in bold numbers (e.g. 3⁴) on sectional chart quadrants?",
            "options": [
                "The elevation of the highest known obstacle or terrain feature in that quadrangle, rounded up plus safety margin",
                "The minimum altitude an ultralight can legally cruise",
                "The average field elevation of all airports in the quadrangle",
                "The radio frequency for flight service"
            ],
            "correct_answer": "The elevation of the highest known obstacle or terrain feature in that quadrangle, rounded up plus safety margin",
            "explanation": "The MEF represents the highest obstacle/terrain feature in thousands and hundreds of feet MSL, rounded up for terrain clearance."
        },
        {
            "question_text": "How does high density altitude affect ultralight takeoff and climb performance?",
            "options": [
                "Longer takeoff ground roll, drastically reduced climb rate, and higher true airspeed at stall",
                "Shorter takeoff roll and steeper climb angle",
                "Engine horsepower increases",
                "Density altitude has no effect on light aircraft"
            ],
            "correct_answer": "Longer takeoff ground roll, drastically reduced climb rate, and higher true airspeed at stall",
            "explanation": "Thin air reduces wing lift, degrades propeller thrust, and robs naturally aspirated engines of horsepower, extending takeoff rolls."
        },
        {
            "question_text": "A temperature-dew point spread of 3°F (1.5°C) or less is a primary indicator of:",
            "options": [
                "Imminent formation of fog or low stratus clouds",
                "Severe turbulence at high altitude",
                "Strong surface tailwinds",
                "High density altitude"
            ],
            "correct_answer": "Imminent formation of fog or low stratus clouds",
            "explanation": "When temperature and dew point converge within 3°F, air reaches 100% relative humidity, causing water vapor to condense into fog or low clouds."
        },
        {
            "question_text": "Why is mid-day flying (between 11:00 AM and 4:00 PM) on hot summer days hazardous for low-inertia ultralights?",
            "options": [
                "Intense solar heating produces strong convective thermal turbulence and dust devils that can exceed control authority",
                "Carb icing is most severe at mid-day",
                "Fuel tanks will boil over",
                "Airspace regulations prohibit mid-day flights"
            ],
            "correct_answer": "Intense solar heating produces strong convective thermal turbulence and dust devils that can exceed control authority",
            "explanation": "Strong thermals and dust devils create violent downdrafts and wind shear that can easily flip or stall low-wing-loading ultralights."
        },

        # =========================================================================
        # SECTION 6: EMERGENCIES, FORCED LANDINGS & AIRPORT PROTOCOLS (Questions 79 - 90)
        # =========================================================================
        {
            "question_text": "Your engine fails at 200 feet AGL immediately after takeoff. What is the correct survival action?",
            "options": [
                "Maintain aircraft control, lower the nose for best glide, and land straight ahead into the wind",
                "Attempt a 180-degree turn back to the runway",
                "Pull back on the control stick to stretch the glide",
                "Turn off the master switch and close your eyes"
            ],
            "correct_answer": "Maintain aircraft control, lower the nose for best glide, and land straight ahead into the wind",
            "explanation": "Attempting the 'impossible turn' back to the runway below 500' AGL leads to a stall/spin. Maintain glide speed and land ahead."
        },
        {
            "question_text": "Why does gliding into a strong headwind drastically reduce your glide distance across the ground during an engine-out descent?",
            "options": [
                "Headwinds reduce groundspeed while the aircraft sinks at its normal descent rate, steepening the glide angle across the ground",
                "Headwinds reduce the aerodynamic lift of the wing",
                "Headwinds cause the engine to windmill backwards",
                "Headwinds increase parasite drag by 50%"
            ],
            "correct_answer": "Headwinds reduce groundspeed while the aircraft sinks at its normal descent rate, steepening the glide angle across the ground",
            "explanation": "Airspeed remains constant, but groundspeed is reduced by the headwind. Less ground covered per minute of descent shrinks the forward glide footprint."
        },
        {
            "question_text": "Why is touching down with a 10-knot tailwind significantly more hazardous than landing into a 10-knot headwind during a forced landing?",
            "options": [
                "Kinetic impact energy is proportional to groundspeed squared (KE = 1/2 m v²), vastly multiplying crash forces",
                "The engine will run hotter",
                "The aircraft cannot turn on rollout",
                "Tailwinds cause the landing gear to collapse instantly"
            ],
            "correct_answer": "Kinetic impact energy is proportional to groundspeed squared (KE = 1/2 m v²), vastly multiplying crash forces",
            "explanation": "Impact forces multiply with the square of groundspeed. An extra 20 knots of groundspeed quadruples impact energy."
        },
        {
            "question_text": "What critical action should be taken regarding the engine before deploying a Ballistic Recovery System (BRS) parachute?",
            "options": [
                "Shut off the engine to prevent the propeller from cutting the deployment bridle or parachute lines",
                "Run the engine at full throttle",
                "Leave the engine at idle",
                "Pump the carburetor primer"
            ],
            "correct_answer": "Shut off the engine to prevent the propeller from cutting the deployment bridle or parachute lines",
            "explanation": "A spinning prop can sever or wrap the parachute risers and canopy lines, causing total deployment failure."
        },
        {
            "question_text": "What is the universal international aviation VHF emergency radio frequency?",
            "options": ["121.5 MHz", "122.8 MHz", "123.45 MHz", "118.0 MHz"],
            "correct_answer": "121.5 MHz",
            "explanation": "121.5 MHz is the international VHF aeronautical emergency guard frequency monitored by ATC and passing aircraft."
        },
        {
            "question_text": "What is the standard traffic pattern entry procedure at a non-towered airport?",
            "options": [
                "Enter at a 45-degree angle to the downwind leg at traffic pattern altitude, midfield",
                "Straight-in approach at full power",
                "Fly directly over the runway at 100 feet AGL",
                "Enter on base leg without announcing"
            ],
            "correct_answer": "Enter at a 45-degree angle to the downwind leg at traffic pattern altitude, midfield",
            "explanation": "Standard recommended traffic pattern entry is at a 45-degree angle to the downwind leg at pattern altitude, intersecting midfield."
        },
        {
            "question_text": "What altitude do ultralights commonly fly in an airport traffic pattern when general aviation aircraft fly at 1,000 feet AGL?",
            "options": [
                "500 feet AGL (lower and tighter inside pattern with prior coordination to maintain separation from faster traffic)",
                "1,500 feet AGL",
                "Same altitude as jets (2,000' AGL)",
                "100 feet AGL"
            ],
            "correct_answer": "500 feet AGL (lower and tighter inside pattern with prior coordination to maintain separation from faster traffic)",
            "explanation": "Ultralights often fly a 500-foot AGL pattern inside the GA pattern to prevent faster aircraft from overrunning them."
        },
        {
            "question_text": "What does a large yellow or white 'X' painted on the threshold of a runway indicate?",
            "options": [
                "The runway is closed to all aircraft operations",
                "The runway is reserved exclusively for ultralights",
                "An emergency helicopter landing spot",
                "A displaced threshold"
            ],
            "correct_answer": "The runway is closed to all aircraft operations",
            "explanation": "An 'X' painted on a runway indicates it is closed and hazardous for landing."
        },
        {
            "question_text": "What does a displaced threshold (marked by white arrows pointing to a solid white line) indicate?",
            "options": [
                "The portion with arrows is usable for taxi and takeoff, but cannot be used for landing touchdown",
                "Landing is permitted on the arrows only",
                "The runway is closed permanently",
                "Reserved for glider winches"
            ],
            "correct_answer": "The portion with arrows is usable for taxi and takeoff, but cannot be used for landing touchdown",
            "explanation": "Displaced thresholds provide obstacle clearance on approach. You may roll out or take off over them, but never land before the solid line."
        },
        {
            "question_text": "What is the primary danger of loose articles (gloves, phones, sectional charts, pins) in a 'pusher' configuration ultralight?",
            "options": [
                "They will be sucked directly into the aft-mounted propeller, causing blade destruction and catastrophic airframe impact",
                "They will jam the elevator cables inside the wing",
                "They will increase parasite drag by 20%",
                "They can distract air traffic control"
            ],
            "correct_answer": "They will be sucked directly into the aft-mounted propeller, causing blade destruction and catastrophic airframe impact",
            "explanation": "In pusher aircraft, anything dropped from the cockpit goes straight into the propeller, shredding blades and throwing debris."
        },
        {
            "question_text": "What personal preflight fitness checklist is recommended by the FAA to assess physical and mental readiness before flight?",
            "options": ["The IMSAFE checklist", "The GUMPS checklist", "The PAVE checklist", "The 5 Cs"],
            "correct_answer": "The IMSAFE checklist",
            "explanation": "IMSAFE stands for Illness, Medication, Stress, Alcohol, Fatigue, and Emotion/Eating."
        },
        {
            "question_text": "Under FAA regulations and aeromedical guidance, what is the rule regarding alcohol consumption before flight?",
            "options": [
                "Minimum 8 hours bottle-to-throttle and less than 0.04% blood alcohol, though 0.00% is professional best practice",
                "2 hours and under 0.08%",
                "Alcohol is permitted if flying only in Class G airspace",
                "12 hours only if drinking hard liquor"
            ],
            "correct_answer": "Minimum 8 hours bottle-to-throttle and less than 0.04% blood alcohol, though 0.00% is professional best practice",
            "explanation": "FAR 91.17 mandates at least 8 hours bottle-to-throttle and blood alcohol below 0.04%. For ultralight flight, 0.00% is the only safe standard."
        }
    ]