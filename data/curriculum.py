"""
data/curriculum.py - Comprehensive ground school study texts.
"""

import textwrap

def get_study_content():
    return {
        "FAR Part 103 Overview": textwrap.dedent("""
            FAR Part 103 governs ultralight vehicles in the United States, established in 1982 to preserve recreational flight with minimal FAA oversight.

            CORE LEGAL PRINCIPLES:
            • No Pilot Certificate: You do not need a pilot license, flight training sign-off, or FAA medical certificate.
            • No Aircraft Registration: The vehicle carries no N-number or tail markings.
            • No Airworthiness Certificate: The FAA does not certify or inspect the structural integrity of the airframe.
            • 100% Pilot Responsibility: The freedom granted by Part 103 means the operator assumes total legal and 
              physical responsibility for their own safety and airworthiness.

            POWERED VEHICLE LIMITS (FAR 103.1):
            1. Single Occupant: Manned by one person only.
            2. Recreation & Sport Only: Commercial flights, advertising, crop dusting, aerial photography for pay, 
               or daily business commuting are strictly prohibited.
            3. Empty Weight: Less than 254 pounds (115 kg), excluding floats and ballistic safety chutes.
            4. Fuel Capacity: Strictly 5 U.S. gallons maximum.
            5. Top Speed: Not capable of exceeding 55 knots (63 mph) calibrated airspeed at full power in level flight.
            6. Stall Speed: Power-off stall speed must not exceed 24 knots (28 mph) calibrated airspeed.

            UNPOWERED VEHICLES (Hang Gliders, Paragliders):
            • Empty Weight: Must weigh less than 155 pounds empty weight.
        """),

        "FAR Part 103 Operations": textwrap.dedent("""
            OPERATIONAL REGULATIONS & FLIGHT RULES:

            • Daylight Flight Only (§103.11): Sunrise to sunset.
              Civil Twilight Exception: Flight is allowed 30 minutes before sunrise and 30 minutes after sunset ONLY IF 
              the vehicle is equipped with an operating anti-collision light visible for at least 3 statute miles, and 
              remains strictly in Class G (uncontrolled) airspace.
            • Hazardous Operation (§103.9): You may not operate in a manner that creates a hazard to persons or property 
              on the surface. Objects may only be dropped if no hazard is created (e.g., wind streamers over empty fields).
            • Congested Areas (§103.15): Flight over any congested area of a city, town, settlement, or open-air assembly 
              of persons (stadiums, concerts, beaches) is strictly prohibited. You must always maintain an unpowered 
              glide path to a safe forced landing site without endangering anyone on the ground.
            • Right-of-Way Rules (§103.13):
              - Ultralights MUST YIELD right-of-way to all other aircraft (airplanes, gliders, balloons, airships).
              - Powered ultralights must yield to unpowered ultralights (hang gliders/paragliders).
              - Head-on: Both aircraft alter course to the right.
              - Overtaking: The overtaking aircraft alters course to the right.
              - Landing: The aircraft on final approach to land has right-of-way.
        """),

        "FAA AC 103-7 Weight Credits": textwrap.dedent("""
            Advisory Circular AC 103-7 provides the FAA's official guidance on Part 103 inspection, weight compliance, 
            and performance calculation methods.

            LEGAL EMPTY WEIGHT EXCLUSIONS:
            The FAA grants specific weight allowances above the 254-lb empty weight limit for safety equipment:
            • Ballistic Parachute Systems (BRS): Up to 24 pounds of credit may be deducted for an installed deployable 
              emergency parachute system.
            • Non-Amphibious Floats: Up to 30 pounds per float may be deducted.
            • Amphibious Floats: Up to 60 pounds total may be deducted to account for wheels and retraction gear.

            WHAT MUST COUNT TOWARD THE 254 LBS?
            Everything else! Radios, GPS units, instruments, windshields, doors, larger tires, wheel pants, and electric 
            starters count toward the 254-lb empty weight.

            FUEL TANK VOLUME COMPLIANCE:
            The 5-gallon fuel rule applies to the physical volume capacity of the tank. Installing an 8-gallon tank and 
            only putting 4 gallons inside is a federal violation.
        """),

        "Four-Stroke Aero Engines: Half-VW & Conversions": textwrap.dedent("""
            FOUR-STROKE AERO ENGINES: THE HALF-VW PHENOMENON

            Origin & Construction:
            The "Half-VW" is a two-cylinder horizontally opposed (flat-twin) four-stroke engine created by slicing a standard 
            air-cooled Volkswagen Type-1 automotive case in half, or casting a dedicated custom two-cylinder aluminum case 
            (popularized by Scott Casler/Hummel Engines, Great Plains, and Better Half VW).

            OPERATING CHARACTERISTICS & ADVANTAGES:
            • Firing Cadence: Boxer twin layout yields smooth horizontal balance with a distinctive 4-stroke thrum.
            • Output: Typically 28 to 37 hp at 3,200 to 3,600 RPM.
            • Direct Drive: Because max power RPM matches propeller efficiency limits, Half-VWs often run direct-drive 
              (no gearbox or belt reduction drive required), swinging 52" to 54" propellers.
            • Fuel Efficiency: Burns standard unmixed avgas or mogas at ~1.8 to 2.5 GPH, providing vastly superior 
              fuel endurance compared to thirsty 2-strokes on a 5-gallon tank.

            CRITICAL 4-STROKE MAINTENANCE & OPERATING HAZARDS:
            1. Valve Lash Maintenance (Solid Lifters):
               Mechanical flat tappets require regular feeler gauge checks. Valve lash must be set COLD, strictly to 
               0.006" (0.15 mm) for both intake and exhaust. Insufficient clearance leads to valve recession, unseated 
               valves during climb-out, and catastrophic valve burning.
            2. Oil Temperature Management:
               - Minimum Safe Oil Temp: 160°F (71°C). Running too cool allows moisture and unburnt fuel acids to contaminate the sump.
               - Maximum Redline Oil Temp: 220°F (104°C). Running hotter breaks down oil film viscosity, leading to bearing destruction.
               - Minimum Cruise Oil Pressure: 25 to 40 PSI.
            3. Cylinder Cooling Baffling:
               Unlike automotive cowls with high-speed ducted fans, an ultralight Half-VW depends on ram air. Tight, pressure-sealed 
               aluminum baffles are required to force cooling air down between cylinder fins. Without tight baffles, the rear cylinder 
               and exhaust valve guides overheat rapidly.
            4. The 254-lb Weight Penalty:
               A complete Half-VW weighs 78 to 88 lbs. Compared to a 55-lb Rotax two-stroke, this eats 25+ extra pounds of your 
               254-lb empty airframe budget! Airframes using Half-VWs (like the Hummel Bird or Legal Eagle) require featherweight 
               wings and empennages to remain legally Part 103 compliant.
        """),

        "Industrial Four-Stroke Conversions (Briggs Vanguard & Kohler V-Twins)": textwrap.dedent("""
            INDUSTRIAL FOUR-STROKE CONVERSIONS (V-TWINS)

            Many ultralight builders convert industrial 90° V-Twin utility engines (Briggs & Stratton Vanguard 627cc to 993cc, 
            Kohler Command Pro, or Predator 670cc) to achieve affordable, reliable 4-stroke power (23 to 35+ hp).

            WHY INDUSTRIAL ENGINES?
            • Automotive-grade reliability, standard push-button electric start, clean fuel burn, and no premix oil hassle.
            • Extremely low acquisition and replacement part costs.

            CONVERSION CHALLENGES & FLIGHT HAZARDS:
            1. Governor Removal & Valve Float:
               Stock industrial engines have mechanical governors capping RPM at 3,600 RPM. For aviation, governors must be 
               bypassed to allow throttle control up to 4,000–4,200 RPM for takeoff.
               HAZARD: Over-revving beyond 4,200 RPM causes severe valve float, throwing pushrods and puncturing pistons. 
               Heavy-duty valve springs are mandatory for converted engines.
            2. Mandatory Propeller Speed Reduction Unit (PSRU):
               Unlike the Half-VW, industrial V-twins produce maximum torque around 3,600 RPM. Turning a prop direct-drive 
               at 3,600 RPM requires small prop diameters with low climb thrust. A 1.6:1 to 2.2:1 cogged belt reduction 
               (e.g., Ace, Valley Engineering) is necessary to turn large 56"-60" props with high static thrust.
            3. Torsional Resonance & Firing Pulses:
               A 90° V-twin produces powerful uneven torque spikes. Without a flexible prop coupling, rubber drive isolator, 
               or centrifugal clutch, these pulses can snap reduction belts, shear flywheel keys, and crack prop hub bolts.
            4. Forced Lubrication & Oil Cooler Requirements:
               Never use a splash-lubricated engine! Only full-pressure lubricated engines with spin-on oil filters and high-volume 
               oil pumps can survive steep nose-up climb attitudes. An external oil cooler is mandatory to prevent thermal runaway.
            5. Weight Budget:
               An industrial V-twin + reduction drive + starter + battery weighs 85 to 98 lbs installed. This leaves under 160 lbs 
               for the entire remainder of the aircraft.
        """),

        "Two-Stroke Engines & Fuel Systems": textwrap.dedent("""
            TWO-STROKE ENGINE SURVIVAL GUIDE

            Most factory ultralights use two-stroke engines (Rotax 447/503/582, Hirth, MZ, Polini). They offer unbeatable 
            power-to-weight ratios but demand proactive thermal management:

            1. Lubrication & Throttle Management:
               In premix engines, fuel carries the lubricating oil.
               CRITICAL TRAP: Closing the throttle during a prolonged, steep power-off descent cuts off lubrication while 
               the engine spins at 5,000+ RPM. Always leave a trickle of throttle or blip the throttle regularly during descent!

            2. Cold Seizures:
               Aluminum pistons expand much faster than cast-iron cylinder liners. Taking off before the engine achieves 
               operating CHT (minimum 250°F / 120°C) will seize the piston against the cylinder walls on initial climb-out.

            3. Ethanol & Phase Separation:
               Automotive pump gasoline containing ethanol attracts ambient water. Phase separation creates an unburnable water-alcohol 
               pool at the bottom of the tank and leans out remaining fuel, causing high Exhaust Gas Temperatures (EGT) and holed pistons.

            4. 5-Gallon Endurance Planning:
               Burning 3.5 to 4.5 gallons per hour provides only 60 to 80 minutes of flight. Always plan to land with a 30-minute reserve.
        """),

        "Airspace for Ultralights": textwrap.dedent("""
            AIRSPACE CLASSIFICATION & ACCESS RULES (§103.17)

            Controlled Airspace Restrictions:
            • Class A (18,000' MSL to FL600): Strictly prohibited to all ultralights.
            • Classes B, C, D, and Class E surface areas for an airport: Ultralights CANNOT enter without prior 
              authorization from the controlling ATC facility. Radio contact alone does not constitute authorization.

            Primary Operating Airspace:
            • Class G (Uncontrolled): The natural home of ultralight flight. Extends from the surface up to 700' or 
              1,200' AGL (and up to 14,500' MSL in remote western areas). No radio, transponder, or ADS-B required.
            • Class E (Controlled): Ultralights can operate in overlying Class E airspace without ATC permission as long 
              as it does not touch the surface at an airport.

            VFR WEATHER MINIMUMS IN CLASS G:
            • 1,200' AGL or Less: 1 statute mile visibility; Remain CLEAR OF CLOUDS.
            • Above 1,200' AGL to 10,000' MSL: 1 statute mile visibility; 500' below, 1,000' above, 2,000' horizontal from clouds.
            • At or Above 10,000' MSL: 5 statute miles visibility; 1,000' below, 1,000' above, 1 SM horizontal.
        """),

        "Basic Weather for VFR Flight": textwrap.dedent("""
            WEATHER DYNAMICS & LOW-INERTIA FLIGHT HAZARDS

            Density Altitude:
            High temperatures, high humidity, and high field elevations thin the air, reducing wing lift and engine horsepower. 
            Takeoff rolls double and climb rates decrease significantly.

            Wind, Shear & Gradients:
            • Surface Friction & Gradients: Wind speed drops near the ground due to terrain friction. When descending on 
              final approach through a wind gradient, your indicated airspeed will drop abruptly.
            • Thermal Turbulence: Peak solar heating (11:00 AM to 5:00 PM) produces strong thermals and dust devils. Ultralights 
              fly safest in smooth early morning and calm late evening air.
            • Temperature-Dew Point Spread: A spread of 3°F (2°C) or less indicates imminent fog or low stratus clouds.
            • Spatial Disorientation: Flying VFR into clouds (IMC) causes fatal spatial disorientation in seconds.
        """),

        "Navigation and Sectional Charts": textwrap.dedent("""
            VFR NAVIGATION FUNDAMENTALS

            • Pilotage: Navigating by matching ground landmarks (roads, rivers, silos, towns) against a VFR Sectional Chart. 
              The primary method for ultralight flying.
            • Dead Reckoning: Calculating groundspeed, heading, and flight time using airspeed, compass, and estimated winds.
            • Maximum Elevation Figure (MEF): The large bold numbers on a sectional quadrant (e.g., 4⁵) indicate the 
              elevation of the highest obstacle or terrain in that quadrant, rounded up to the nearest 100 feet plus safety margin.
            • Sectional Airport Colors: Blue = Towered Airport (Class B, C, D); Magenta = Non-towered Airport (Class E, G).
            • The 5 Cs for Lost Procedures: Climb, Circle, Conserve, Communicate (121.5 MHz), Confess.
        """),

        "Airport Operations and Markings": textwrap.dedent("""
            AIRPORT OPERATIONS & TRAFFIC PATTERNS

            • Standard Pattern: Standard pattern uses left-hand turns at 1,000' AGL for general aviation. Ultralights frequently 
              fly a tighter, lower pattern (500' AGL) with prior coordination to avoid faster aircraft.
            • Pattern Legs: Upwind -> Crosswind -> Downwind -> Base -> Final approach. Enter at a 45-degree angle to the downwind leg.
            • Runway Numbering: Numbered by magnetic heading to the nearest 10 degrees (e.g., Runway 27 = 270°).
            • Displaced Threshold: Marked by white arrows leading to a solid white line. Usable for taxi and takeoff, prohibited for landing.
            • Closed Runway: Marked by large yellow or white 'X's at both ends.
            • Radio Protocol: Handheld radios on CTAF (Common Traffic Advisory Frequency) are critical for announcing intentions.
        """),

        "Aerodynamics & Low Wing Loading": textwrap.dedent("""
            AERODYNAMIC PHENOMENA & CRITICAL TRAPS

            The Aerodynamic Stall:
            • Occurs when the critical Angle of Attack (AOA) is exceeded. Airflow separates from the upper wing, causing lift to collapse.
            • A stall can happen at ANY airspeed and ANY flight attitude.
            • Recovery: Immediately push the control stick forward to lower the angle of attack below critical.

            The Deadly Base-to-Final Turn:
            • Overshooting final approach leads pilots to apply inside rudder without banking (skidding turn).
            • The outside wing travels faster and produces more lift; the inside wing stalls first.
            • Result: A violent, unrecoverable spin at 300 feet AGL. Never use rudder to skid toward the centerline—go around!

            Wake Turbulence Vulnerability:
            • Ultralights have extremely low wing loading (3 to 6 lbs/sq ft). A wake vortex from even a small Cessna 172 can invert an 
              ultralight in milliseconds, exceeding control authority. Avoid landing behind larger aircraft.
        """),

        "Weight, Balance & Control Types": textwrap.dedent("""
            WEIGHT & BALANCE AND CONTROL CONFIGURATIONS

            Extreme Weight Sensitivity:
            Because the empty airframe weighs only 254 lbs, a 200-lb pilot represents over 40% of gross flight weight. Small variations 
            in pilot weight or luggage push the Center of Gravity (CG) drastically.
            • Aft CG Danger: An aft CG reduces pitch stability, making stall and spin recovery aerodynamically impossible.

            Control Configurations:
            1. Three-Axis (Fixed Wing): Conventional stick and rudder.
            2. Weight-Shift Control (Trikes):
               REVERSED CONTROLS:
               • Pushing the bar FORWARD shifts pilot weight aft -> pitches the wing UP (slows down/climbs).
               • Pulling the bar AFT pitches the wing DOWN (accelerates/descends).
               • Pushing the bar RIGHT tilts the wing LEFT -> initiates a LEFT turn.
               Three-axis pilots transitioning to trikes must undergo dual instruction to override panic muscle memory!
            3. Powered Paragliders (PPG):
               Susceptible to motor torque twist and pendulum oscillations. Never release brake toggles near the ground.
        """),

        "Ultralight Systems & Preflight": textwrap.dedent("""
            PREFLIGHT INSPECTION PROTOCOLS

            • Pusher Configuration Warning:
              Anything loose in the cockpit (gloves, maps, phones, cameras, pins) will blow back directly into the propeller, causing blade 
              failure or airframe destruction.
            • Structural Tubing: Inspect aluminum tubes for distortion, elongation around bolt holes, and hairline cracks near engine mounts.
            • Sailcloth & Stitching: UV radiation degrades Dacron fabric. Test fabric strength periodically using a Maule punch tester.
            • Pre-flight Fuel Sump: Drain fuel from the lowest sump point into a clear cup to verify absence of water, debris, or phase separation.
            • Ballistic Chute Pin: Ensure the safety pin is REMOVED before takeoff and the activation handle is reachable.
        """),

        "Human Factors (ADM & IMSAFE)": textwrap.dedent("""
            AERONAUTICAL DECISION MAKING (ADM)

            Hazardous Attitudes & Antidotes:
            1. Anti-Authority ("Don't tell me"): Follow the rules; they are usually right.
            2. Impulsivity ("Do it quickly"): Not so fast; think first.
            3. Invulnerability ("It won't happen to me"): It could happen to me.
            4. Macho ("I can do it"): Taking chances is foolish.
            5. Resignation ("What's the use?"): I am not helpless; I can make a difference.

            Personal Fitness (IMSAFE):
            Illness, Medication, Stress, Alcohol (8 hours bottle-to-throttle / 0.04% BAC, though 0.00% is best practice), Fatigue, Emotion/Eating.
        """),

        "Emergency Procedures & Survival": textwrap.dedent("""
            EMERGENCY ACTION PLANS

            Aviate, Navigate, Communicate:
            Fly the plane first!

            Engine Failure on Takeoff:
            • Never attempt the "impossible turn" back to the runway below 500' AGL.
            • Lower the nose immediately to maintain glide speed and land straight ahead into the wind.

            Engine Failure at Altitude (A-B-C-D-E):
            • A - Airspeed: Pitch for Best Glide (L/D max).
            • B - Best Field: Select landing area within glide cone; plan for an upwind landing.
            • C - Checklist: Quick scan (fuel valve, switches), but never sacrifice aircraft control.
            • D - Declare: Mayday on 121.5 MHz or CTAF if radio equipped.
            • E - Execute: Fly the pattern to the field; commit to touchdown.

            Ballistic Chute Deployment:
            If structural failure occurs or the aircraft enters an unrecoverable spin, shut off the engine (to avoid fouling lines) and firmly pull the BRS activation handle.
        """)
    }