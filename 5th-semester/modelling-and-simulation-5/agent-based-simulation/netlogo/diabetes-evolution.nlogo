;;;; Initialization
breed [risks risk] ;; turtles at risk
breed [diabetesp diabetes] ;; turtles with diabetes
breed [healthyp healthy] ;; turtles healthy
turtles-own [
  glucose ;; turtles eat food and increase/decrease glucose
  sex ;; turtles own a gender, 0 man and 1 woman.
  marry ;; turtles are married
  related ;; proportion of marriage people
  sp ;; stores social pressure by relevant others
  bmi ;; body mass index
  age ;; age for wedding ring
  change ;; change tick
]
patches-own [ health ;; representing healthy food
  unhealthy ;; representing unhealthy food
]


;;;; Setup
to setup
  clear-all
  setup-patches ;; JSC: Removed random number for patches.

  create-healthyp initial-healthy ;; represent people without diabetes in a population
  [   set shape "person"
      set size 2
      set color green
      set glucose 80 + random 20.5 ;; mg/dL, these values represent true clinical serum blood values of fasting glucose levels
      set sex random 1.5
      set marry 0
      set age (21 + random 13.5)
      set bmi (18.5 + random-float 6.4)
      set change 0
      setxy random-xcor random-ycor
  ]

  create-diabetesp initial-diabetes ;; represent people with diabetes in a population
  [   set shape "person"
      set size 2
      set color red
      set glucose 120 + random 10.5 ;; mg/dL
      set sex random 1.5
      set marry 0
      set age (21 + random 12.5)
      set change 0

      ;; Choice of bmi
      let choice random 100
      let probs (list 0.5 12.2 10.3 17.8 26.1 15.5 17.6)
      let bmis (list (list 15 18.5) (list 18.6 24.9) (list 25 26.9) (list 27 27.9) (list 30 34.9) (list 35 39.9) (list 40 60))
      let sum0 0
      let index 0
      let bmi0 1
      while [index < length probs] [
            let elem (item index probs)
            set sum0 (sum0 + elem)
            if choice < sum0 [
               let elem0 (item index bmis)
               set bmi0 ((item 0 elem0) + random-float ((item 1 elem0) - (item 0 elem0)))
               set index (length probs)
            ]
            set index (index + 1)
      ]
      set bmi bmi0
      setxy random-xcor random-ycor
  ]

  create-risks initial-risk ;; represent people who are at risk of diabetes in a population
  [   set shape "person"
      set size 2
      set color yellow
      set glucose 105 + random 15.5 ;;mg/dL
      set sex random 1.5
      set marry 0
      set age (20 + random 13.5)
      set bmi (25 + random-float 4.9)
      set change 0
      setxy random-xcor random-ycor
  ] ;; JSC: Changed initial glucose values.

  ask turtles [
    let n (int ((count turtles) / 10))
    ifelse n > 0
           [set related (n-of n turtles)]
           [set related (n-of 1 turtles)]
  ]
  reset-ticks
end

;;;; Tick logic
to go
  ;; Diabetes interaction
  ask healthyp [
      move-turtles
      change-turtles
      change-status
  ]

  ask risks [
      move-turtles
      healthy-turtles
      change-status
  ]

  ask diabetesp [
      move-turtles
      healthy-turtles
      change-status
  ]

  ;; Wedding ring
  ask healthyp [
      ifelse marry = 0
             [choose_marriage]
             [divorce]
  ]

  ask risks [
      ifelse marry = 0
             [choose_marriage]
             [divorce]
  ]

  ask diabetesp [
      ifelse marry = 0
             [choose_marriage]
             [divorce]
  ]
  if ticks > 1500 [ stop ]
  tick
end ;; JSC: Removed junk code.

to change-turtles
   eat-unhealthy
   if glucose > 105 [
      set color yellow
   ]
   if glucose >= 120 [
      set color red
   ]
end

to healthy-turtles
   eat-healthy
   if glucose > 105 and glucose < 120 [
      set color yellow
  ]
   if glucose < 100 [
      set color green
   ]
end

to move-turtles
   rt random 50
   lt random 50
   fd 1
end


to eat-unhealthy
   ; people eat unhealthy, turn patches black
   ifelse pcolor = pink
          [set pcolor black
           set glucose glucose - 1] ;; mg/dL
          [set glucose glucose + 1]
end

to eat-healthy
   ; people eat healthier, turn patches pink
   ifelse pcolor = black
          [set pcolor pink
           set glucose glucose + 1] ; mg/dL
          [set glucose glucose - 1]
end

to setup-patches
   ask patches [set pcolor pink]
end

;;;; Wedding ring interaction functions
to choose_marriage
  ;; Change bmi
  ifelse sex = 0
         [set bmi (max (list 15 (bmi - 0.6 + random-float 0.66)))]
         [set bmi (max (list 15 (bmi - 0.9 + random-float 0.54)))]

  ;; Calculate pom
  let pom0 (count related with [marry > 0])
  let pom (pom0 / (count related))

  ;; Calculate social pressure
  let alpha 0.5
  let beta 7
  set sp (exp(beta * (pom - alpha)) / (1 + exp(beta *(pom - alpha))))

  ;; Choose partner
  let N (count turtles)
  let age0 age
  let c 25
  let ai 0.875
  let d0 (sp * ai * c)
  let found false
  let num who
  let marry0 0
  ask turtles in-radius (sp * 50 * 50 * ai / N) with [marry = 0] [
      if (age0 - d0 < age) and (age < age0 + d0) and (num != who) [
         set marry0 (2 + random 25)
         set marry marry0
         set found true
         set change 3
         stop
      ]
  ]
  if found [
     set change 3
     set marry marry0
  ]
end

to divorce
  set marry (marry - 1)
  ifelse change = 0 [
         set change 3
         ifelse sex = 0
                [set bmi (min (list 60 (bmi + 0.46 + random-float 0.48)))]
                [set bmi (min (list 60 (bmi + 0.66 + random-float 0.6)))]
  ]
         [set change (change - 1)]
end

to change-status
   let probs (list 3.2 13 4.4 5.7 11.1 16.5 46.1)
   let bmis (list (list 15 18.5) (list 18.6 24.9) (list 25 26.9) (list 27 27.9) (list 30 34.9) (list 35 39.9) (list 40 60))
   let choice (random 100)
   let index 0
   while [index < length bmis] [
         let elem (item index bmis)
         if (item 0 elem) < bmi and bmi < (item 1 elem) [
            let prob (item index probs)
            ifelse choice < prob [
                   set color red
                   set index (length bmis)
            ][
                   set color green
                   set index (length bmis)
            ]
         ]
         set index (index + 1)
   ]
end
@#$#@#$#@
GRAPHICS-WINDOW
216
13
653
451
-1
-1
13.0
1
10
1
1
1
0
1
1
1
-16
16
-16
16
0
0
1
ticks
30.0

BUTTON
31
10
97
43
NIL
setup
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

BUTTON
120
11
183
44
NIL
go
T
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

SLIDER
18
86
190
119
initial-healthy
initial-healthy
0
100
71.0
1
1
NIL
HORIZONTAL

SLIDER
17
129
189
162
initial-diabetes
initial-diabetes
0
100
29.0
1
1
NIL
HORIZONTAL

PLOT
686
15
873
162
People with Diabetes
NIL
NIL
0.0
10.0
0.0
10.0
true
false
"" ""
PENS
"default" 1.0 0 -2674135 true "" "plot count turtles with [color = red]"

SLIDER
16
174
188
207
initial-risk
initial-risk
0
100
10.0
1
1
NIL
HORIZONTAL

PLOT
686
168
875
315
People at Risk
NIL
NIL
0.0
10.0
0.0
10.0
true
false
"" ""
PENS
"default" 1.0 0 -1184463 true "" "plot count turtles with [color = yellow]"

PLOT
688
321
876
446
Healthy People
NIL
NIL
0.0
10.0
0.0
10.0
true
false
"" ""
PENS
"default" 1.0 0 -13840069 true "" "plot count turtles with [color = green]"

BUTTON
46
220
156
253
Unhealthy
eat-unhealthy
NIL
1
T
TURTLE
NIL
NIL
NIL
NIL
1

TEXTBOX
46
257
196
313
Indicates increased consumption of unhealthy foods correlated with diabetes incidence.
11
0.0
1

BUTTON
40
324
156
357
Healthy
eat-healthy
NIL
1
T
TURTLE
NIL
NIL
NIL
NIL
1

TEXTBOX
38
361
188
431
Indicates decreased consumption of unhealthy foods correlated with diabetes incidence.
11
0.0
1

PLOT
880
15
1067
162
Married people
NIL
NIL
0.0
10.0
0.0
10.0
true
false
"" ""
PENS
"default" 1.0 0 -13345367 true "" "plot count turtles with [marry > 0]"

PLOT
880
169
1069
316
Average BMI
NIL
NIL
0.0
10.0
0.0
10.0
true
false
"" ""
PENS
"default" 1.0 0 -7858858 true "" "plot mean [bmi] of turtles"

@#$#@#$#@
## WHAT IS IT?

This model is showing the incidence of diabetes in the United States as set within particular clinical parameters for fasting glucose levels. Each year, approximately 1 in 10 adult Americans are diagnosed with diabetes, and currently, roughly 10% of the U.S. population is living with the disease. This model hopes to act as a visual aid to show the impact of this disease on the population as so many people are affected, or rather, are at risk and may go undiagnosed for years until they find out too late.

## HOW IT WORKS

The model begins by setting up the amount of people globally in a population. At the start, 300 people are able to start off in the global environment. Depending on what the user of this model would like to specifically model will determine how many people start off either healthy (absence of diabetes), at risk, or has diabetes. Use the sliders to determine those amounts of people. Whether a person falls under these aforementioned categories depends on particular fasting glucose amounts as practiced clinically. Diabetes (>120mg/dL), at risk (105-120mg/dL), and healthy (<105 mg/dL). These were the rules presented in the code to define these populations. The plots to the right of the interface show the rise and fall of people with diabetes to place a numeric value on the amount of people in each category. The patches represent eating a healthy diet versus eating a diet which is shown to be a risk factor for diabetes incidence (high fat/sugar). Pink represents eating a healthy diet, black patches represent eating an unhealthy diet. The red people in the interface represent those with diabetes; yellow indicates at risk, and green indicates healthy. There are "unhealthy" and "healthy" buttons which are turtle-only commands which allow the user of the model to manually adjust the parameters for eating a healthy diet versus an unhealthy diet.

## HOW TO USE IT

The buttons "setup", "go once" and "go" will act as the model starters. There are three sliders, "initial-diabetes", "initial-healthy" and "initial-risk" which shows the amount of people who are starting out as either diagnosed with diabetes, healthy, or at risk for developing diabetes. Click on the "go once" button to see slowly the progession of people either getting diabetes, becomnig at risk, or regressing from diabetes and becoming healthy. Click "go" to watch in real-time the overlap of peolpe eating healthy, unhealthy, getting diabetes, becoming at risk, or getting healthier. Watch the plots as they spike up and down or grow steady as time goes on.

## THINGS TO NOTICE
Notice as glucose levels rise, the incidence of diabetes is more prevalent, and as glucose levels fall (eat-healthy) the incidence of diabetes is not as prevalent, but either remains steady or even decreases. The more people with diabetes will mean the more red and yellow people, and less green people, and vice versa. Notice the plots changing, increasing up and down as they correlate with these fluctuations.

## THINGS TO TRY

Try clicking on the "healthy" and "unhealthy" buttons to manually force the amount of uneahlthy eating habits or healthy eating habits and notice the changes in diabetes prevalence and incidence in the global environment. Try scaling the amount of people who intially have diabetes, who are at risk, or who are healthy. This will adjust the amount of time it takes for everyone to be at risk for diabetes or who have diabetes.

## EXTENDING THE MODEL

Try extending the model to adjust the patches to be more fluid, or make a segmented version of the global environment to portray possibly different demographic or geographic locations of food deserts or those who are of low SES. This could help model health disparities and differences amongst populations. Another extension could be to include more parameters that act as either risk factors or risk reducers, such as physical activity.

## NETLOGO FEATURES

Special NetLogo features include the use of setting the turtle parametes and patches colors. The language in of itself is unique to this model, but it made it simple to set the parameters and rules that I needed in order to help this model come to fruition.

## RELATED MODELS

There is a model which shows blood glucose levels and insulin resistance, titled "Blood Sguar Regulation". I did not use much, if at all, of this code, but it did help me create this idea to make it more applicable to real life situations, such as incidence of disease. This model is related to blood glucose levels, however does not show prevalence or incidence of diabetes specifically.

## CREDITS AND REFERENCES

Blood Sugar Regulation model that gave me this idea: http://ccl.northwestern.edu/netlogo/models/BloodSugarRegulation

Credit to Dr. Garcia of Arizona State University who introduced NetLogo to our class and allowed us the opportunity to learn a new skill that can be applied in scientific research, especially in systems thinking.
@#$#@#$#@
default
true
0
Polygon -7500403 true true 150 5 40 250 150 205 260 250

airplane
true
0
Polygon -7500403 true true 150 0 135 15 120 60 120 105 15 165 15 195 120 180 135 240 105 270 120 285 150 270 180 285 210 270 165 240 180 180 285 195 285 165 180 105 180 60 165 15

arrow
true
0
Polygon -7500403 true true 150 0 0 150 105 150 105 293 195 293 195 150 300 150

box
false
0
Polygon -7500403 true true 150 285 285 225 285 75 150 135
Polygon -7500403 true true 150 135 15 75 150 15 285 75
Polygon -7500403 true true 15 75 15 225 150 285 150 135
Line -16777216 false 150 285 150 135
Line -16777216 false 150 135 15 75
Line -16777216 false 150 135 285 75

bug
true
0
Circle -7500403 true true 96 182 108
Circle -7500403 true true 110 127 80
Circle -7500403 true true 110 75 80
Line -7500403 true 150 100 80 30
Line -7500403 true 150 100 220 30

butterfly
true
0
Polygon -7500403 true true 150 165 209 199 225 225 225 255 195 270 165 255 150 240
Polygon -7500403 true true 150 165 89 198 75 225 75 255 105 270 135 255 150 240
Polygon -7500403 true true 139 148 100 105 55 90 25 90 10 105 10 135 25 180 40 195 85 194 139 163
Polygon -7500403 true true 162 150 200 105 245 90 275 90 290 105 290 135 275 180 260 195 215 195 162 165
Polygon -16777216 true false 150 255 135 225 120 150 135 120 150 105 165 120 180 150 165 225
Circle -16777216 true false 135 90 30
Line -16777216 false 150 105 195 60
Line -16777216 false 150 105 105 60

car
false
0
Polygon -7500403 true true 300 180 279 164 261 144 240 135 226 132 213 106 203 84 185 63 159 50 135 50 75 60 0 150 0 165 0 225 300 225 300 180
Circle -16777216 true false 180 180 90
Circle -16777216 true false 30 180 90
Polygon -16777216 true false 162 80 132 78 134 135 209 135 194 105 189 96 180 89
Circle -7500403 true true 47 195 58
Circle -7500403 true true 195 195 58

circle
false
0
Circle -7500403 true true 0 0 300

circle 2
false
0
Circle -7500403 true true 0 0 300
Circle -16777216 true false 30 30 240

cow
false
0
Polygon -7500403 true true 200 193 197 249 179 249 177 196 166 187 140 189 93 191 78 179 72 211 49 209 48 181 37 149 25 120 25 89 45 72 103 84 179 75 198 76 252 64 272 81 293 103 285 121 255 121 242 118 224 167
Polygon -7500403 true true 73 210 86 251 62 249 48 208
Polygon -7500403 true true 25 114 16 195 9 204 23 213 25 200 39 123

cylinder
false
0
Circle -7500403 true true 0 0 300

dot
false
0
Circle -7500403 true true 90 90 120

face happy
false
0
Circle -7500403 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 255 90 239 62 213 47 191 67 179 90 203 109 218 150 225 192 218 210 203 227 181 251 194 236 217 212 240

face neutral
false
0
Circle -7500403 true true 8 7 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Rectangle -16777216 true false 60 195 240 225

face sad
false
0
Circle -7500403 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 168 90 184 62 210 47 232 67 244 90 220 109 205 150 198 192 205 210 220 227 242 251 229 236 206 212 183

fish
false
0
Polygon -1 true false 44 131 21 87 15 86 0 120 15 150 0 180 13 214 20 212 45 166
Polygon -1 true false 135 195 119 235 95 218 76 210 46 204 60 165
Polygon -1 true false 75 45 83 77 71 103 86 114 166 78 135 60
Polygon -7500403 true true 30 136 151 77 226 81 280 119 292 146 292 160 287 170 270 195 195 210 151 212 30 166
Circle -16777216 true false 215 106 30

flag
false
0
Rectangle -7500403 true true 60 15 75 300
Polygon -7500403 true true 90 150 270 90 90 30
Line -7500403 true 75 135 90 135
Line -7500403 true 75 45 90 45

flower
false
0
Polygon -10899396 true false 135 120 165 165 180 210 180 240 150 300 165 300 195 240 195 195 165 135
Circle -7500403 true true 85 132 38
Circle -7500403 true true 130 147 38
Circle -7500403 true true 192 85 38
Circle -7500403 true true 85 40 38
Circle -7500403 true true 177 40 38
Circle -7500403 true true 177 132 38
Circle -7500403 true true 70 85 38
Circle -7500403 true true 130 25 38
Circle -7500403 true true 96 51 108
Circle -16777216 true false 113 68 74
Polygon -10899396 true false 189 233 219 188 249 173 279 188 234 218
Polygon -10899396 true false 180 255 150 210 105 210 75 240 135 240

house
false
0
Rectangle -7500403 true true 45 120 255 285
Rectangle -16777216 true false 120 210 180 285
Polygon -7500403 true true 15 120 150 15 285 120
Line -16777216 false 30 120 270 120

leaf
false
0
Polygon -7500403 true true 150 210 135 195 120 210 60 210 30 195 60 180 60 165 15 135 30 120 15 105 40 104 45 90 60 90 90 105 105 120 120 120 105 60 120 60 135 30 150 15 165 30 180 60 195 60 180 120 195 120 210 105 240 90 255 90 263 104 285 105 270 120 285 135 240 165 240 180 270 195 240 210 180 210 165 195
Polygon -7500403 true true 135 195 135 240 120 255 105 255 105 285 135 285 165 240 165 195

line
true
0
Line -7500403 true 150 0 150 300

line half
true
0
Line -7500403 true 150 0 150 150

pentagon
false
0
Polygon -7500403 true true 150 15 15 120 60 285 240 285 285 120

person
false
0
Circle -7500403 true true 110 5 80
Polygon -7500403 true true 105 90 120 195 90 285 105 300 135 300 150 225 165 300 195 300 210 285 180 195 195 90
Rectangle -7500403 true true 127 79 172 94
Polygon -7500403 true true 195 90 240 150 225 180 165 105
Polygon -7500403 true true 105 90 60 150 75 180 135 105

plant
false
0
Rectangle -7500403 true true 135 90 165 300
Polygon -7500403 true true 135 255 90 210 45 195 75 255 135 285
Polygon -7500403 true true 165 255 210 210 255 195 225 255 165 285
Polygon -7500403 true true 135 180 90 135 45 120 75 180 135 210
Polygon -7500403 true true 165 180 165 210 225 180 255 120 210 135
Polygon -7500403 true true 135 105 90 60 45 45 75 105 135 135
Polygon -7500403 true true 165 105 165 135 225 105 255 45 210 60
Polygon -7500403 true true 135 90 120 45 150 15 180 45 165 90

sheep
false
15
Circle -1 true true 203 65 88
Circle -1 true true 70 65 162
Circle -1 true true 150 105 120
Polygon -7500403 true false 218 120 240 165 255 165 278 120
Circle -7500403 true false 214 72 67
Rectangle -1 true true 164 223 179 298
Polygon -1 true true 45 285 30 285 30 240 15 195 45 210
Circle -1 true true 3 83 150
Rectangle -1 true true 65 221 80 296
Polygon -1 true true 195 285 210 285 210 240 240 210 195 210
Polygon -7500403 true false 276 85 285 105 302 99 294 83
Polygon -7500403 true false 219 85 210 105 193 99 201 83

square
false
0
Rectangle -7500403 true true 30 30 270 270

square 2
false
0
Rectangle -7500403 true true 30 30 270 270
Rectangle -16777216 true false 60 60 240 240

star
false
0
Polygon -7500403 true true 151 1 185 108 298 108 207 175 242 282 151 216 59 282 94 175 3 108 116 108

target
false
0
Circle -7500403 true true 0 0 300
Circle -16777216 true false 30 30 240
Circle -7500403 true true 60 60 180
Circle -16777216 true false 90 90 120
Circle -7500403 true true 120 120 60

tree
false
0
Circle -7500403 true true 118 3 94
Rectangle -6459832 true false 120 195 180 300
Circle -7500403 true true 65 21 108
Circle -7500403 true true 116 41 127
Circle -7500403 true true 45 90 120
Circle -7500403 true true 104 74 152

triangle
false
0
Polygon -7500403 true true 150 30 15 255 285 255

triangle 2
false
0
Polygon -7500403 true true 150 30 15 255 285 255
Polygon -16777216 true false 151 99 225 223 75 224

truck
false
0
Rectangle -7500403 true true 4 45 195 187
Polygon -7500403 true true 296 193 296 150 259 134 244 104 208 104 207 194
Rectangle -1 true false 195 60 195 105
Polygon -16777216 true false 238 112 252 141 219 141 218 112
Circle -16777216 true false 234 174 42
Rectangle -7500403 true true 181 185 214 194
Circle -16777216 true false 144 174 42
Circle -16777216 true false 24 174 42
Circle -7500403 false true 24 174 42
Circle -7500403 false true 144 174 42
Circle -7500403 false true 234 174 42

turtle
true
0
Polygon -10899396 true false 215 204 240 233 246 254 228 266 215 252 193 210
Polygon -10899396 true false 195 90 225 75 245 75 260 89 269 108 261 124 240 105 225 105 210 105
Polygon -10899396 true false 105 90 75 75 55 75 40 89 31 108 39 124 60 105 75 105 90 105
Polygon -10899396 true false 132 85 134 64 107 51 108 17 150 2 192 18 192 52 169 65 172 87
Polygon -10899396 true false 85 204 60 233 54 254 72 266 85 252 107 210
Polygon -7500403 true true 119 75 179 75 209 101 224 135 220 225 175 261 128 261 81 224 74 135 88 99

wheel
false
0
Circle -7500403 true true 3 3 294
Circle -16777216 true false 30 30 240
Line -7500403 true 150 285 150 15
Line -7500403 true 15 150 285 150
Circle -7500403 true true 120 120 60
Line -7500403 true 216 40 79 269
Line -7500403 true 40 84 269 221
Line -7500403 true 40 216 269 79
Line -7500403 true 84 40 221 269

wolf
false
0
Polygon -16777216 true false 253 133 245 131 245 133
Polygon -7500403 true true 2 194 13 197 30 191 38 193 38 205 20 226 20 257 27 265 38 266 40 260 31 253 31 230 60 206 68 198 75 209 66 228 65 243 82 261 84 268 100 267 103 261 77 239 79 231 100 207 98 196 119 201 143 202 160 195 166 210 172 213 173 238 167 251 160 248 154 265 169 264 178 247 186 240 198 260 200 271 217 271 219 262 207 258 195 230 192 198 210 184 227 164 242 144 259 145 284 151 277 141 293 140 299 134 297 127 273 119 270 105
Polygon -7500403 true true -1 195 14 180 36 166 40 153 53 140 82 131 134 133 159 126 188 115 227 108 236 102 238 98 268 86 269 92 281 87 269 103 269 113

x
false
0
Polygon -7500403 true true 270 75 225 30 30 225 75 270
Polygon -7500403 true true 30 75 75 30 270 225 225 270
@#$#@#$#@
NetLogo 6.0.4
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
default
0.0
-0.2 0 0.0 1.0
0.0 1 1.0 0.0
0.2 0 0.0 1.0
link direction
true
0
Line -7500403 true 150 150 90 180
Line -7500403 true 150 150 210 180
@#$#@#$#@
0
@#$#@#$#@
