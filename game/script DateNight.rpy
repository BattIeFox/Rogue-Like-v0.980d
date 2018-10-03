# Date Night //////////////////////////////////////////////////////////////////////
# Gets called from the Events whenever "yesdate" in P_DailyActions
# Checks to see which girls show up, if more than one, they decide whether they are cool with that.
# If they are, you choose location. You can go to dinner first, or skip to movies.
# During dinner there is a check to menu, then a check to whether sexy stuff occurs
# During sexy stuff, the other girl can join in, ignore it, ot cockblock it. 
# Then you pay, during which you can cause offense by being cheap.
# Then you can pick a movie, and pay for that too, similar to dinner. 
# Then you watch the movie and potentially have sex, and again the other girl can object. 
# Then you return to campus, and can pick a girl to take home first, the other will follow. 

label DateNight(Prime_Bonus=0,Second_Bonus=0,Play_Cost=0,Prime_Cost=0,Second_Cost=0):
    # Called from the event menu    
    # Party[0] is the lead girl Party[1] the other. 
    # P_Bonus and S_Bonus track the girl's love bonuses, Cost is cost of the date
    
    $ Party = [] #clears Party if there is one
    
    if "yesdate" in R_DailyActions:  #Checks if Rogue is in
            $ Party.append("Rogue")
            $ R_DailyActions.remove("yesdate")
    if "yesdate" in K_DailyActions:  #Checks if Kitty is in
            $ Party.append("Kitty")
            $ K_DailyActions.remove("yesdate")    
    if "yesdate" in E_DailyActions:  #Checks if Emma is in
            $ Party.append("Emma")
            $ E_DailyActions.remove("yesdate")
    
    if not Party:
            "Nobody showed up, weird."
            return
       
    $ renpy.random.shuffle(Party)
    
    while len(Party) > 2:        
            # If two or more members in the party    
            #Culls down party size to two
            $ Party.remove(Party[2])
            
        
    # This portion sets the girls' clothing and mood for the date
    if "Rogue" in Party:  
                call Rogue_Date_Prep
    if "Kitty" in Party:  
                call Kitty_Date_Prep
    if "Emma" in Party:  
                call Emma_Date_Prep
                               
    $ bg_current = "date" 
    call Shift_Focus(Party[0])
    call Set_The_Scene     
        
    if len(Party)== 2:
        "As you arrive, you see [Party[0]] and [Party[1]] waiting for you."
        call Date_Crossed
        if not Party: 
                # both left
                return
        elif len(Party) < 2:
            # One stayed, but not both
            ch_p "Ok then, I guess we're ready to get going. . ."            
            $ Party.append(0)
    else:
        "As you arrive, you see [Party[0]] waiting for you."          
        $ Party.append(0)
        
    if "Rogue" in Party and "stoodup" in R_History:
                $ R_History.remove("stoodup") 
    if "Kitty" in Party and "stoodup" in K_History:
                $ K_History.remove("stoodup") 
    if "Emma" in Party and "stoodup" in E_History:
                $ E_History.remove("stoodup") 
            
    if Party[0] == "Rogue":
        ch_r "Where are we going?"
    elif Party[0] == "Kitty":
        ch_k "So[K_like]where would you like to go?"
    elif Party[0] == "Emma":
        ch_e "Did you have a place in mind?"
    
    menu:
        extend ""
        "To a restaurant.":
            $ P_RecentActions.append("dinner")                      
            $ P_DailyActions.append("dinner") 
        "To the movies.":
            $ P_RecentActions.append("movie")                      
            $ P_DailyActions.append("movie") 
        "Dinner and a movie.": 
            $ P_RecentActions.append("dinner")                      
            $ P_DailyActions.append("dinner") 
            $ P_RecentActions.append("movie")                      
            $ P_DailyActions.append("movie")
                    
    if Party[1] == "Rogue" or (Party[0] == "Rogue" and not Party[1]):
        ch_r "Sounds fun."
    elif Party[1] == "Kitty" or (Party[0] == "Kitty" and not Party[1]):
        ch_k "K, let's get going then."
    elif Party[1] == "Emma" or (Party[0] == "Emma" and not Party[1]):
        ch_e "Oh, lovely, shall we?"
            
    show blackscreen onlayer black with dissolve
            
    if "dinner" not in P_RecentActions:
        "You head to the local theater and check out the film listings."
        jump Date_Movies
    else:
        "You go to one of the nicer restaurants in town. The food is quality but reasonably affordable." 
        jump Date_Dinner

#End Date Start   / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / /
    
    
    
#Start Crossed Wires Sequence   / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / /
    
label Date_Crossed(Girls=[],Check=0,CrossedP=0,CrossedS=0,Count=0):
    #this checks to make sure both girls are on the same page. 
    if Party[0] == "Rogue" and "yesdouble" not in R_DailyActions:
        ch_r "What's [Party[1]] doing here?"
        $ Girls.append("Rogue")
    elif Party[0] == "Kitty" and "yesdouble" not in K_DailyActions:
        ch_k "Huh? What's [Party[1]] doing here?"
        $ Girls.append("Kitty")
    elif Party[0] == "Emma" and "yesdouble" not in E_DailyActions:
        ch_e "Oh, hello, why is [Party[1]] here?"
        $ Girls.append("Emma")
        
    if Party[1] == "Rogue" and "yesdouble" not in R_DailyActions:
        if Girls:
            ch_r "Yeah, why's [Party[0]] here?"
        else:
            ch_r "What's [Party[0]] doing here?"
        $ Girls.append("Rogue")
    elif Party[1] == "Kitty" and "yesdouble" not in K_DailyActions:
        if Girls:
            ch_k "Yeah, what gives?"
        else:
            ch_k "Huh? What's [Party[0]] doing here?"
        $ Girls.append("Kitty")
    elif Party[1] == "Emma" and "yesdouble" not in E_DailyActions:
        if Girls:
            ch_e "Yes, care to explain?"
        else:
            ch_e "Oh, hello, why is [Party[0]] here?"
        $ Girls.append("Emma")
            
    if not Girls:
        return
        
    menu:
        "I thought we could have fun together.":
            $ Check = "fun"
        "Oh, I forgot to tell you?":
            $ Check = "cute"  
        "You're both coming with me.":
            $ Check = "order"
            
        "Never mind [[ditch one or both]":
                menu:
                    "Rogue, you can go" if "Rogue" in Party:
                            if ApprovalCheck("Rogue", 1400, "LO"):
                                call RogueFace("sad", 1)
                                ch_r "Oh, ok, I guess. Later then?"
                                "Rogue heads off."
                                call Rogue_Date_Over(0)
                            else:
                                call Rogue_Date_Over                
                    "Kitty, you can go" if "Kitty" in Party:
                            if ApprovalCheck("Kitty", 1400, "LO"):
                                call EmmaFace("sad", 1)
                                ch_k "Huh? Well, ok, I guess?"
                                "Kitty heads off."
                                call Kitty_Date_Over(0)
                            else:
                                call Kitty_Date_Over        
                    "Emma, you can go" if "Emma" in Party:
                            if ApprovalCheck("Emma", 1500, "LO"):
                                call EmmaFace("sad", 1)
                                ch_e "Hm. You'll have to make this up to me later."
                                "Emma walks off."
                                call Emma_Date_Over(0)
                            else:
                                call Emma_Date_Over  
                    "Never mind. [[Go home]": 
                            if "Rogue" in Party:
                                    if ApprovalCheck("Rogue", 1400, "LO"):
                                        call RogueFace("sad", 1)
                                        ch_r "Oh, ok, I guess. Later then?"
                                        call Rogue_Date_Over(0)
                                    else:
                                        call Rogue_Date_Over                
                            if "Kitty" in Party:
                                    if ApprovalCheck("Kitty", 1400, "LO"):
                                        call EmmaFace("sad", 1)
                                        ch_k "Huh? Well, ok, I guess?"
                                        call Kitty_Date_Over(0)
                                    else:
                                        call Kitty_Date_Over        
                            if "Emma" in Party:
                                    if ApprovalCheck("Emma", 1500, "LO"):
                                        call EmmaFace("sad", 1)
                                        ch_e "Hm. You'll have to make this up to me later."
                                        call Emma_Date_Over(0)
                                    else:
                                        call Emma_Date_Over  
                            "You head back to your room."
                            if "yesdate" in P_DailyActions:
                                    $ P_DailyActions.remove("yesdate")
                            $ renpy.pop_call() 
                            $ renpy.pop_call()   
                            jump Player_Room                                
                return #?
                $ Check = "ditch"
    #end question menu
    
    if Party[0] == "Rogue":
            if Party[1] == "Kitty":
                    $ CrossedP = R_LikeKitty
                    $ CrossedS = K_LikeRogue                  
            elif Party[1] == "Emma":
                    $ CrossedP = R_LikeKitty
                    $ CrossedS = K_LikeRogue  
    elif Party[0] == "Kitty":
            if Party[1] == "Rogue":
                    $ CrossedP = K_LikeRogue  
                    $ CrossedS = R_LikeKitty                
            elif Party[1] == "Emma":
                    $ CrossedP = K_LikeEmma
                    $ CrossedS = E_LikeKitty
    elif Party[0] == "Emma":                
            if Party[1] == "Rogue":
                    $ CrossedP = E_LikeRogue
                    $ CrossedS = R_LikeEmma
            elif Party[1] == "Kitty":
                    $ CrossedP = E_LikeKitty
                    $ CrossedS = K_LikeEmma 
    
    if "Rogue" in Girls:
            if not Party[1]:
                #if the other girl's dropped out
                if not ApprovalCheck("Rogue", 1000):
                    ch_r "So. . . I'm going to get going too?"
                    call Rogue_Date_Over(0)
                return                
                    
            if Party[0] == "Rogue":
                $ Count = CrossedP
            else:
                $ Count = CrossedS
               
            if Check == "fun":
                    if ApprovalCheck("Rogue",1000):
                        $ Check = 0
                    else:
                        $ Check = -200
            elif Check == "cute":  
                    if ApprovalCheck("Rogue",1000,"LI"):
                        $ Check = 200
                    else:
                        $ Check = -100
            elif Check == "order":
                    if ApprovalCheck("Rogue",1200,"LO"):
                        $ Check = 100
                    else:
                        $ Check = -300
            else:
                        $ Check = 0
            
            if Count >= 600 and ApprovalCheck("Rogue", 800, "OI", Bonus = Check): #Count is "K_LikeX"
                call RogueFace("smile")
                ch_r "Sure, why not."                                
            elif Count >= 750:
                call RogueFace("bemused")
                ch_r "Oh, I guess. . ."                                
            elif ApprovalCheck("Rogue", 1300, "LO", Bonus = Check): 
                call RogueFace("sad")
                ch_r "If you insist. . ."             
            else:
                call RogueFace("angry")
                ch_r "In your dreams!"  
                call Rogue_Date_Over(0)
            #End Rogue check
                
    if "Kitty" in Girls:
            if not Party[1]:
                #if the other girl's dropped out
                if not ApprovalCheck("Kitty", 1000):
                    ch_k "Yeah, this is kind of a weird scene, maybe I'll see you later?"
                    call Kitty_Date_Over(0)
                return                
                    
            if Party[0] == "Kitty":
                $ Count = CrossedP
            else:
                $ Count = CrossedS
               
            if Check == "fun":
                    if ApprovalCheck("Kitty",1000):
                        $ Check = 0
                    else:
                        $ Check = -200
            elif Check == "cute":  
                    if ApprovalCheck("Kitty",1000,"LI"):
                        $ Check = 100
                    else:
                        $ Check = -100
            elif Check == "order":
                    if ApprovalCheck("Kitty",1200,"LO"):
                        $ Check = 200
                    else:
                        $ Check = -300
            else:
                        $ Check = 0
            
            if Count >= 600 and ApprovalCheck("Kitty", 800, "OI", Bonus = Check): #Count is "K_LikeX"
                call KittyFace("smile")
                ch_k "Sure, sounds fun."                                
            elif Count >= 750:
                call KittyFace("bemused")
                ch_k "Hm, yeah. . ."                                
            elif ApprovalCheck("Kitty", 1300, "LO", Bonus = Check): 
                call KittyFace("sad")
                ch_k "I guess if that's what you want. . ."             
            else:
                call KittyFace("angry")
                ch_k "You wish, player!"  
                call Kitty_Date_Over(0)
            #End Kitty check
            
    if "Emma" in Girls:
            if not Party[1]:
                #if the other girl's dropped out
                if not ApprovalCheck("Emma", 800):
                    ch_e "Unprofessional, but I do give you points for trying."
                    call Emma_Date_Over(0)
                return                
                    
            if Party[0] == "Emma":
                $ Count = CrossedP
            else:
                $ Count = CrossedS
               
            if Check == "fun":
                    if ApprovalCheck("Emma",1000):
                        $ Check = 100
                    else:
                        $ Check = -100
            elif Check == "cute":  
                    if ApprovalCheck("Emma",1000,"LI"):
                        $ Check = 100
                    else:
                        $ Check = 0
            elif Check == "order":
                    if ApprovalCheck("Emma",1200,"LO"):
                        $ Check = 300
                    else:
                        $ Check = -400
            else:
                        $ Check = 0
            
            if Count >= 600 and ApprovalCheck("Emma", 800, "OI", Bonus = Check): #Count is "K_LikeX"
                call EmmaFace("sly")
                ch_e "This could be interesting. . ."                                
            elif Count >= 750:
                call EmmaFace("sly")
                ch_e "Alright, I'm in"                                
            elif ApprovalCheck("Emma", 1300, "LO", Bonus = Check): 
                call EmmaFace("sad")
                ch_e "If you insist."             
            else:
                call EmmaFace("surprised",Mouth="smirk")
                ch_e "Oh, you do aim high."
                call EmmaFace("angry")
                ch_e "Too high."
                call Emma_Date_Over(0)
            #End Emma check
                       
    return
#End Crossed Wires Sequence   / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / /
    
#Start Dinner Sequence   / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / /
label Date_Dinner:    
    $ bg_current = "bg restaurant"
    if "Rogue" in Party:
            $ R_Loc = "bg restaurant"
    if "Kitty" in Party:
            $ K_Loc = "bg restaurant"
    if "Emma" in Party:
            $ E_Loc = "bg restaurant"
    call Set_The_Scene
    
    "The waitress comes to the table."
    
    if "Rogue" in Party:
            call Rogue_Dinner
    if "Kitty" in Party:
            call Kitty_Dinner
    if "Emma" in Party:
            call Emma_Dinner
    call Player_Dinner
               
    "After a bit, the waitress brings you your meals."
    
    $ Line = "You eat your " + Line
    
    if "Kitty" in Party and "surfturf" in K_RecentActions: 
            $ Line = Line + ", Kitty eats the steak but pushes the lobster to the side."
    else:
            $ Line = Line + ", and have a pleasant conversation over the meal."
             
    "[Line]"    
    $ P_RecentActions.append("dinner") 
    
    call Date_Sex("dinner")
    
    call Date_Paying("dinner") 
    
    if not Party[0] and not Party[1]:
            "You decide to head back to your room."
            jump Date_Over

    if "movie" not in P_RecentActions:
            jump Date_End
            
    #else:    
    "After dinner, you head to the local theater and check out the film listings."   
    jump Date_Movies
    
    
# End Primary Dinner Sequence / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / /


        
label Player_Dinner:
    # This is the player's menu choices
    menu:
        "For yourself, you order. . ."
        "Surf and turf. ($20)":
            $ Play_Cost = 20
            $ Line = "steak and a juicy lobster"
        "Steak. ($15)":  
            $ Play_Cost = 15
            $ Line = "medium rare ribeye"
        "Chicken. ($10)":
            $ Play_Cost = 10
            $ Line = "pangrilled chicken thighs"
        "Just a salad. ($5)":
            $ Play_Cost = 5
            $ Line = "fresh garden salad"
    return

#Start Date_Sex   / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / 
label Date_Sex(Activity="dinner",Options = []):
    #This determines who, if any, has sex with the player during the date
        
    if "Rogue" in Party and ApprovalCheck("Rogue", 1000):  #Checks if Rogue is in
            $ Options.append("Rogue")   
            if Party[0] == "Rogue"  and Prime_Bonus > 10:
                    $ Options.append("Rogue")
            elif Party[1] == "Rogue" and Second_Bonus > 10:
                    $ Options.append("Rogue")
            if P_RecentActions in ("horror","drama"):
                    $ Options.append("Rogue")
    if "Kitty" in Party and ApprovalCheck("Kitty", 1000):  #Checks if Kitty is in
            $ Options.append("Kitty") 
            if Party[0] == "Kitty" and Prime_Bonus > 10:
                    $ Options.append("Kitty")
            elif Party[1] == "Kitty" and Second_Bonus > 10:
                    $ Options.append("Kitty")    
            if P_RecentActions in ("horror","drama"):
                    $ Options.append("Kitty")
    if "Emma" in Party and ApprovalCheck("Emma", 1000):  #Checks if Emma is in
            $ Options.append("Emma")
            if Party[0] == "Emma" and Prime_Bonus > 10:
                    $ Options.append("Emma")
            elif Party[1] == "Emma" and Second_Bonus > 10:
                    $ Options.append("Emma")
            if P_RecentActions in ("horror","drama"):
                    $ Options.append("Emma")
    
    if len(Options) == 0:
            "Nobody showed up, weird."
            return
        
    $ renpy.random.shuffle(Options)
    if Options[0] == "Rogue": 
            if Activity == "dinner":
                    call Rogue_Dinner_Sex(Options)
            else:
                    call Rogue_Movie_Sex(Options)
    elif Options[0] == "Kitty":  
            if Activity == "dinner":
                    call Kitty_Dinner_Sex(Options)
            else:
                    call Kitty_Movie_Sex(Options)
    elif Options[0] == "Emma":  
            if Activity == "dinner":
                    call Emma_Dinner_Sex(Options)
            else:
                    call Emma_Movie_Sex(Options)
    return
#end Date_Sex   / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / 

        
#Start Date_Sex_Break   / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / /
label Date_Sex_Break(Lead=0,Previous=0,Repeat=0):
    #Lead is the lead girl
    #Previous is the other girl
    # if it returns 0, it continues normally.
    # if it returns 1, the other girl joins in
    # if it returns 2, the other girl watches
    # if it returns 3, the other girl is mad, but it goes on
    # if it returns 4, the other girl is mad, so you cancel out
    
    if not Previous:
        return 0
    if Lead == "Rogue":
            if Previous == "Kitty":
                if R_LikeKitty >= 700 and K_LikeRogue >= 700:
                        #They like each other and will share
                        $ K_RecentActions.append("noticed rogue")
                        return 1
                elif ApprovalCheck("Kitty", 1400) and K_LikeRogue >= 500:
                        #Kitty likes you, and likes Rogue enough to be chill
                        call KittyFace("sly")
                        "Kitty winks at you, but doesn't move to get involved."
                        $ K_RecentActions.append("noticed rogue")
                        return 2
                elif ApprovalCheck("Kitty", 1400) and K_LikeRogue < 500:
                       pass
                #End if Previous == "Rogue"
            elif Previous == "Emma":
                if R_LikeEmma >= 700 and E_LikeRogue >= 700:
                        #They like each other and will share
                        $ E_RecentActions.append("noticed rogue")
                        return 1
                elif ApprovalCheck("Emma", 1400) and E_LikeRogue >= 500:
                        #Emma likes you, and likes Rogue enough to be chill
                        call EmmaFace("sly")
                        "Emma winks at you, but doesn't move to get involved."
                        $ E_RecentActions.append("noticed rogue")
                        return 2
                elif ApprovalCheck("Emma", 1400) and E_LikeRogue < 500:
                        #Emma likes you, but hates Rogue
                        pass
                #End if Previous == "Emma"
    #End Lead Rogue
    elif Lead == "Kitty":
            if Previous == "Rogue":
                if K_LikeRogue >= 700 and R_LikeKitty >= 700:
                        #They like each other and will share
                        $ R_RecentActions.append("noticed kitty")
                        return 1
                elif ApprovalCheck("Rogue", 1400) and R_LikeKitty >= 500:
                        #Rogue likes you, and likes Kitty enough to be chill
                        call RogueFace("sly")
                        "Rogue winks at you, but doesn't move to get involved."
                        $ R_RecentActions.append("noticed kitty")
                        return 2
                elif ApprovalCheck("Rogue", 1400) and R_LikeKitty < 500:
                       pass
                #End if Previous == "Rogue"
            elif Previous == "Emma":
                if K_LikeEmma >= 700 and E_LikeKitty >= 700:
                        #They like each other and will share
                        $ E_RecentActions.append("noticed kitty")
                        return 1
                elif ApprovalCheck("Emma", 1400) and E_LikeKitty >= 500:
                        #Emma likes you, and likes Kitty enough to be chill
                        call EmmaFace("sly")
                        "Emma winks at you, but doesn't move to get involved."
                        $ E_RecentActions.append("noticed kitty")
                        return 2
                elif ApprovalCheck("Emma", 1400) and E_LikeKitty < 500:
                        #Emma likes you, but hates Kitty
                        pass
                #End if Previous == "Emma"
    #End Lead Kitty
    elif Lead == "Emma":
            if Previous == "Rogue":
                if K_LikeRogue >= 700 and R_LikeKitty >= 700:
                        #They like each other and will share
                        $ R_RecentActions.append("noticed emma")
                        return 1
                elif ApprovalCheck("Rogue", 1400) and R_LikeKitty >= 500:
                        #Rogue likes you, and likes Kitty enough to be chill
                        call RogueFace("sly")
                        "Rogue winks at you, but doesn't move to get involved."
                        $ R_RecentActions.append("noticed emma")
                        return 2
                elif ApprovalCheck("Rogue", 1400) and R_LikeKitty < 500:
                       pass
                #End if Previous == "Rogue"
            elif Previous == "Kitty":
                if E_LikeKitty >= 700 and K_LikeEmma >= 700:
                        #They like each other and will share
                        $ K_RecentActions.append("noticed emma")
                        return 1
                elif ApprovalCheck("Kitty", 1400) and K_LikeEmma >= 500:
                        #Kitty likes you, and likes Emma enough to be chill
                        call KittyFace("sly")
                        "Kitty winks at you, but doesn't move to get involved."
                        $ K_RecentActions.append("noticed emma")
                        return 2
                elif ApprovalCheck("Kitty", 1400) and K_LikeEmma < 500:
                        #Kitty likes you, but hates Emma
                        pass
                #End if Previous == "Emma"
    #End Lead Emma
    
    
    #If they asked you to stop
    if Previous == "Rogue":
            #Rogue likes you, but hates the girl
            if Repeat == 2:
                    #if it's a good night kiss
                    call RogueFace("angry",Eyes="side")
                    $ R_Love = Statupdate("Rogue", "Love", R_Love, 80, -5)
                    $ R_Obed = Statupdate("Rogue", "Obed", R_Obed, 80, 5)
                    return 3                       
            elif Repeat:
                    call RogueFace("angry")
                    $ R_Love = Statupdate("Rogue", "Love", R_Love, 80, -15)
                    $ R_Obed = Statupdate("Rogue", "Obed", R_Obed, 80, 15)
                    ch_r "Get a room you two!"
                    call Rogue_Date_Over
                    # You do it anyway
                    return 3       
            menu:
                ch_r "I know what she's up to, cut it out."
                "Ok, I'll stop.":
                    $ R_Love = Statupdate("Rogue", "Love", R_Love, 80, 10)
                    $ R_Obed = Statupdate("Rogue", "Obed", R_Obed, 80, -5)
                    $ R_Inbt = Statupdate("Rogue", "Inbt", R_Inbt, 60, 5)
                    call Date_Bonus("Rogue",5)
                    # You stop
                    return 4 
                "I don't think so.":
                    call RogueFace("angry")
                    $ R_Love = Statupdate("Rogue", "Love", R_Love, 80, -10)
                    $ R_Obed = Statupdate("Rogue", "Obed", R_Obed, 80, 10)
                    $ R_Inbt = Statupdate("Rogue", "Inbt", R_Inbt, 60, -5)
                    call Date_Bonus("Rogue",-5) 
                    # You do it anyway
                    return 3                            
    elif Previous == "Kitty":
            #Kitty likes you, but hates the girl
            if Repeat == 2:
                    #if it's a good night kiss
                    call KittyFace("angry",Eyes="side")
                    $ K_Love = Statupdate("Kitty", "Love", K_Love, 80, -10)
                    $ K_Obed = Statupdate("Kitty", "Obed", K_Obed, 80, 5)
                    return 3                       
            elif Repeat:
                    call KittyFace("angry")
                    $ K_Love = Statupdate("Kitty", "Love", K_Love, 80, -15)
                    $ K_Obed = Statupdate("Kitty", "Obed", K_Obed, 80, 17)
                    ch_k "Geeze, right in front of me?!"
                    call Kitty_Date_Over
                    # You do it anyway
                    return 3    
            menu:
                ch_k "I see you there, cut it out."
                "Ok.":
                    $ K_Love = Statupdate("Kitty", "Love", K_Love, 80, 12)
                    $ K_Inbt = Statupdate("Kitty", "Inbt", K_Inbt, 60, 5)
                    call Date_Bonus("Kitty",5)
                    # You stop
                    return 4 
                "I don't think so.":
                    call KittyFace("angry")
                    $ K_Love = Statupdate("Kitty", "Love", K_Love, 80, -12)
                    $ K_Obed = Statupdate("Kitty", "Obed", K_Obed, 80, 15)
                    $ K_Inbt = Statupdate("Kitty", "Inbt", K_Inbt, 60, 3)
                    call Date_Bonus("Kitty",-5)
                    # You do it anyway
                    return 3    
    elif Previous == "Emma":
            #Emma likes you, but hates the girl
            if Repeat == 2:
                    #if it's a good night kiss
                    call EmmaFace("angry",Eyes="side")
                    $ E_Love = Statupdate("Emma", "Love", E_Love, 80, -5)
                    $ E_Obed = Statupdate("Emma", "Obed", E_Obed, 80, 10)
                    return 3                       
            elif Repeat:
                    call EmmaFace("angry")
                    $ E_Love = Statupdate("Emma", "Love", E_Love, 80, -10)
                    $ E_Obed = Statupdate("Emma", "Obed", E_Obed, 80, 15)
                    ch_e "Oh do grow up, you two!"
                    call Emma_Date_Over
                    # You do it anyway
                    return 3
            menu:
                ch_e "Oh, I see what's going on, stop it."
                "Ok.":
                    $ E_Love = Statupdate("Emma", "Love", E_Love, 80, 7)
                    $ E_Obed = Statupdate("Emma", "Obed", E_Obed, 80, -2)
                    $ E_Inbt = Statupdate("Emma", "Inbt", E_Inbt, 60, 5)
                    call Date_Bonus("Emma",5)
                    # You stop
                    return 4 
                "I don't think so.":
                    call EmmaFace("angry")
                    $ E_Love = Statupdate("Emma", "Love", E_Love, 80, -7)
                    $ E_Obed = Statupdate("Emma", "Obed", E_Obed, 80, 12)
                    call Date_Bonus("Emma",-5)
                    # You do it anyway
                    return 3
    return 0 #Yes
    
#end Date_Sex_Break   / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / 
        
        
#Start Movie Sequence   / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / /        
label Date_Movies:  
    #This picks and watches a movie
    $ bg_current = "bg movies"
    if "Rogue" in Party:
            $ R_Loc = "bg movies"
    if "Kitty" in Party:
            $ K_Loc = "bg movies"
    if "Emma" in Party:
            $ E_Loc = "bg movies"            
    call Set_The_Scene 
    
    menu:
        "What would you like to see?"
        "A romantic comedy.":
            $ Line = "romcom"
            $ P_RecentActions.append("romcom")
        "An action movie.":
            $ Line = "action"
            $ P_RecentActions.append("action")
        "A horror movie.":
            $ Line = "horror"
            $ P_RecentActions.append("horror")
        "An acclaimed drama.":
            $ Line = "drama" 
            $ P_RecentActions.append("drama")
        "Let Rogue pick." if "Rogue" in Party:
            $ Line = "pick"
            $ Trigger = "Rogue"
        "Let Kitty pick." if "Kitty" in Party:
            $ Line = "pick"
            $ Trigger = "Kitty"
        "Let Emma pick." if "Emma" in Party:
            $ Line = "pick"
            $ Trigger = "Emma"
    
    
    if Line == "pick":
            #if you let one of the girls pick the movie
            if Trigger == "Rogue":
                    call RogueFace("smile")           
                    $ R_Love = Statupdate("Rogue", "Love", R_Love, 80, 4)
                    $ R_Obed = Statupdate("Rogue", "Obed", R_Obed, 50, -2)
                    $ R_Inbt = Statupdate("Rogue", "Inbt", R_Inbt, 50, 2)  
                    ch_r "How sweet, [R_Petname]. Let's see the romantic comedy." 
                    call Date_Bonus("Rogue",20)
                    $ Line = "romcom" 
                    $ P_RecentActions.append("romcom")
            elif Trigger == "Kitty":
                    call KittyFace("smile")  
                    $ K_Love = Statupdate("Kitty", "Love", K_Love, 80, 4)
                    $ K_Obed = Statupdate("Kitty", "Obed", K_Obed, 50, -2)
                    $ K_Inbt = Statupdate("Kitty", "Inbt", K_Inbt, 50, 2) 
                    ch_k "Aw, [K_Petname]. Let's see the drama."          
                    call Date_Bonus("Kitty",20)
                    $ Line = "drama" 
                    $ P_RecentActions.append("drama") 
            elif Trigger == "Emma":
                    call EmmaFace("smile")   
                    $ E_Love = Statupdate("Emma", "Love", E_Love, 80, 5)
                    $ E_Obed = Statupdate("Emma", "Obed", E_Obed, 50, -3)
                    $ E_Inbt = Statupdate("Emma", "Inbt", E_Inbt, 50, 3) 
                    ch_e "Oh, lovely. Let's see the horror film."         
                    call Date_Bonus("Emma",20)
                    $ Line = "horror" 
                    $ P_RecentActions.append("horror") 
    
    if Line == "romcom":
            if "Rogue" in Party and Trigger != "Rogue":
                    call RogueFace("smile", Eyes="surprised")
                    $ R_Love = Statupdate("Rogue", "Love", R_Love, 50, 2)
                    $ R_Love = Statupdate("Rogue", "Love", R_Love, 95, 4)
                    $ R_Inbt = Statupdate("Rogue", "Inbt", R_Inbt, 50, 2)
                    ch_r "Oooh, I love a good rom-com, [R_Petname]. This should be great!"  
                    call Date_Bonus("Rogue",15)
            if "Kitty" in Party and Trigger != "Kitty":
                    call KittyFace("smile", Eyes="surprised")
                    $ K_Love = Statupdate("Kitty", "Love", K_Love, 50, 2)
                    $ K_Love = Statupdate("Kitty", "Love", K_Love, 95, 3)
                    ch_k "Aw, how cuuuute!"   
                    call Date_Bonus("Kitty",5)
            if "Emma" in Party and Trigger != "Emma":
                    call EmmaFace("confused", Mouth="sad")
                    $ E_Love = Statupdate("Emma", "Love", E_Love, 70, 2)
                    $ E_Obed = Statupdate("Emma", "Obed", E_Obed, 50, 5)
                    $ E_Inbt = Statupdate("Emma", "Inbt", E_Inbt, 70, -3)
                    ch_e "How. . . pedestrian."   
                    call Date_Bonus("Emma",-5)
    elif Line == "action":
            if "Rogue" in Party and Trigger != "Rogue":
                    call RogueFace("sexy")
                    ch_r "Hmm, you know I'm always up for some action." 
                    $ R_Love = Statupdate("Rogue", "Love", R_Love, 95, 3)
                    call Date_Bonus("Rogue",5)
            if "Kitty" in Party and Trigger != "Kitty":
                    call KittyFace("sexy")
                    $ K_Love = Statupdate("Kitty", "Love", K_Love, 95, 4)
                    $ K_Inbt = Statupdate("Kitty", "Inbt", K_Inbt, 50, 2)
                    ch_k "Action movies are kind of fun." 
                    call Date_Bonus("Kitty",5)
            if "Emma" in Party and Trigger != "Emma":
                    call EmmaFace("sadside", Brows="angry")
                    $ E_Love = Statupdate("Emma", "Love", E_Love, 70, -2)
                    $ E_Obed = Statupdate("Emma", "Obed", E_Obed, 50, 5)
                    ch_e "I suppose it will at least keep me occupied."          
                    # call Date_Bonus("Emma",0)
    elif Line == "horror":
            if "Rogue" in Party and Trigger != "Rogue":
                    call RogueFace("sad", Eyes="surprised")
                    $ R_Love = Statupdate("Rogue", "Love", R_Love, 90, -3)
                    $ R_Obed = Statupdate("Rogue", "Obed", R_Obed, 50, 3)
                    $ R_Obed = Statupdate("Rogue", "Obed", R_Obed, 80, 2)
                    ch_r "I'm not really into the spooky stuff, [R_Petname]."   
                    # call Date_Bonus("Rogue",0)
            if "Kitty" in Party and Trigger != "Kitty":
                    call KittyFace("sad", Eyes="surprised")      
                    $ K_Love = Statupdate("Kitty", "Love", K_Love, 90, -5)
                    $ K_Obed = Statupdate("Kitty", "Obed", K_Obed, 50, 4)
                    $ K_Obed = Statupdate("Kitty", "Obed", K_Obed, 80, 2)
                    ch_k "It won't be {i}too{/i} scary, right?"          
                    call Date_Bonus("Kitty",-5)
            if "Emma" in Party and Trigger != "Emma":
                    call EmmaFace("sly")
                    $ E_Love = Statupdate("Emma", "Love", E_Love, 70, 3)
                    $ E_Obed = Statupdate("Emma", "Obed", E_Obed, 50, 3)
                    $ E_Inbt = Statupdate("Emma", "Inbt", E_Inbt, 70, 2)
                    $ E_Lust = Statupdate("Emma", "Lust", E_Lust, 60, 5)
                    ch_e "I do love to get a good chill up the spine."          
                    call Date_Bonus("Emma",15)
    elif Line == "drama":
            if "Rogue" in Party and Trigger != "Rogue":
                    call RogueFace("bemused")
                    $ R_Love = Statupdate("Rogue", "Love", R_Love, 95, 1)
                    $ R_Obed = Statupdate("Rogue", "Obed", R_Obed, 50, 3)
                    ch_r "Hmmm, I have heard some good things about this one, could be interesting."   
                    call Date_Bonus("Rogue",5)
            if "Kitty" in Party and Trigger != "Kitty":
                    call KittyFace("bemused")
                    $ K_Love = Statupdate("Kitty", "Love", K_Love, 95, 3)
                    $ K_Obed = Statupdate("Kitty", "Obed", K_Obed, 50, 2)
                    ch_k "I heard this was a good one!"   
                    call Date_Bonus("Kitty",15)
            if "Emma" in Party and Trigger != "Emma":
                    call EmmaFace("normal")
                    $ E_Love = Statupdate("Emma", "Love", E_Love, 70, 2)
                    $ E_Obed = Statupdate("Emma", "Obed", E_Obed, 50, 3)
                    ch_e "Ah, this does sound like an interesting one."          
                    call Date_Bonus("Emma",5)    
    $ Trigger = 0
    
    call Date_Paying("movie")   
    
    if not Party[0] and not Party[1]:
            #if you're ditched,
            "You decide to watch the movie anyway, but it was pretty boring."
            "Afterwards you just head back to your room."
            jump Date_Over
    
    $ P_RecentActions.append("movie") 
    #The movie plays.
    if Party[1]:
        "You take your seat in between the other two."
    else:
        "You take your seats in the theater."
        
    if "romcom" in P_RecentActions:    
        $ Line = renpy.random.choice(["You watch the movie, which is about an adorkable girl who can't choose between two hunky guys. She picks the other one.", 
                    "You watch the movie, which is about a girl who is mercilessly stalked by some weird guy, until she eventually decides she loves him. They live hapily ever after.", 
                    "In this movie, the lead goes to all her friend's weddings, but can't get it together herself. She dies alone. Just kidding, she gets married at the end.", 
                    "You watch the movie, in which a bunch of college girls go on a wild adventure and have lots of random sex.",
                    "This movie is about a girl who's convinced to live in a sex dungeon, and really seems to enjoy it.",
                    "This movie is about a girl who works for a fashion house and is bullied by her boss, until they become friends."])        
    elif "action" in P_RecentActions: 
        $ Line = renpy.random.choice(["You watch the movie, which is about an ex marine fighting aliens.", 
                    "You watch the movie, which is about a girl who is mercilessly stalked by some weird guy, until she eventually decides she loves him. They live hapily ever after. There are also a lot of explosions.", 
                    "In this movie, giant robots are fighting animal mash-ups, with the fate of the world in the balance.", 
                    "You watch the movie, in which a team of non-mutant superhumans are apparently fighting some sort of silvery robots in Eastern Europe.",
                    "This movie is about a superhuman powerhouse that nearly wrecks a town, and yet is not arrested for it by the humans. Must be the hammer.",
                    "This movie is about 90 minutes of constant explosions and lensflares."])
    elif "horror" in P_RecentActions: 
        $ Line = renpy.random.choice(["You watch the movie, which is about an adorkable girl who can't choose between two hunky guys. She picks the other one. The guys are a fishman and a skeleton.", 
                    "You watch the movie, which is about a girl who is mercilessly stalked by some weird guy, until she eventually gives in and marries him. Her life is an endless hell.", 
                    "In this movie, a group of teens are trapped in a wilderness cabin. They have a lot of random sex as some shadowy monster kills them one by one.", 
                    "In this movie, a group of teens are trapped in an abandoned motel. They have a lot of random sex as some shadowy monster kills them one by one.", 
                    "This movie is about a girl who's convinced to live in a sex dungeon, and she's eventually murdered.",
                    "In this movie, a group of teens are trapped in a spaceship. They have a lot of random sex as some shadowy monster kills them one by one."])
    elif "drama" in P_RecentActions: 
        $ Line = renpy.random.choice(["You watch the movie, which is about a mature woman who can't choose between two eligible widowers. She picks the other one.", 
                    "You watch the movie, which is a documentary about a girl who is mercilessly stalked by some weird guy, until she eventually decides she gets a restraining order.", 
                    "In this movie, which is a biopic about a great historical leader.", 
                    "You watch the movie, in which a disabled person struggles with his various disabilities, and eventually overcomes them, and/or dies.",
                    "This movie is about a lot of yelling and crying as some very serious issues are explored by an ensemble cast."])
   
    "[Line]" #You watch the movie. . .
    
    call Date_Sex("movie")
                
    jump Date_End
        
#end Movie Sequence  / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / 
               
#Start Payment system   / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / /         
label Date_Paying(Activity="dinner", Total_Cost=0):  
    # Activity is which thing you're doing, total cost is the combined meal costs. 
    if Activity == "dinner":
                $ Total_Cost = Play_Cost + Prime_Cost + Second_Cost
                "The Waitress brings you the check, it comes to $[Total_Cost]."
    else:
        if Party[1]:
                $ Total_Cost = 30
                "You go to the ticket window, three tickets would be $30."
        else:
                $ Total_Cost = 20
                "You go to the ticket window, two tickets would be $20."
                
    menu:
        "Who's paying?"
        "I've got it." if P_Cash >= Total_Cost:
            $ Line = "you"         
                        
        "Rogue, you pay." if "Rogue" in Party:    
            $ Line = "Rogue"                 
        "Kitty, you pay." if "Kitty" in Party:    
            $ Line = "Kitty"  
        "Emma, you pay." if "Emma" in Party:    
            $ Line = "Emma"                                          
                
        "Let's split it." if P_Cash >= Play_Cost:   
            $ Line = "split"                             
                        
        "I really can't afford it. . ." if P_Cash < Total_Cost: 
            $ Line = "deadbeat"    
    
    if Line == "you":
            #If you offer to cover the meal
            if "Rogue" in Party:
                    if "deadbeat" in R_History:  
                        $ R_History.remove("deadbeat") 
                    call RogueFace("sexy", 1)
                    ch_r "Oh, and such a gentleman."
                    $ R_Love = Statupdate("Rogue", "Love", R_Love, 50, 2)
                    $ R_Love = Statupdate("Rogue", "Love", R_Love, 80, 2) 
                    if Total_Cost >= 15: 
                        $ R_Love = Statupdate("Rogue", "Love", R_Love, 200, 2)
                    $ P_Cash -= Total_Cost                    
                    call Date_Bonus("Rogue",Total_Cost)
                    
            if "Kitty" in Party:
                    if "deadbeat" in K_History:  
                        $ K_History.remove("deadbeat") 
                    call KittyFace("sexy", 1)
                    ch_k "[K_Like]that's really nice of you."
                    $ K_Love = Statupdate("Kitty", "Love", K_Love, 50, 2)
                    $ K_Love = Statupdate("Kitty", "Love", K_Love, 80, 2) 
                    if Total_Cost >= 15: 
                        $ K_Love = Statupdate("Kitty", "Love", K_Love, 200, 2)
                    $ P_Cash -= Total_Cost                    
                    call Date_Bonus("Kitty",Total_Cost)
                    
            if "Emma" in Party:
                    if "deadbeat" in E_History:  
                        $ E_History.remove("deadbeat") 
                    call EmmaFace("sly", 1)
                    ch_e "Oh, how very mature of you."
                    $ E_Obed = Statupdate("Emma", "Obed", E_Obed, 50, 3)
                    $ E_Love = Statupdate("Emma", "Love", E_Love, 50, 2) 
                    $ E_Love = Statupdate("Emma", "Love", E_Love, 80, 2) 
                    if Total_Cost >= 15: 
                        $ E_Love = Statupdate("Emma", "Love", E_Love, 200, 2)
                    $ P_Cash -= Total_Cost                    
                    call Date_Bonus("Emma",Total_Cost)
                   
    elif Line == "Rogue":  
            #If you ask Rogue to pay
            $ R_Love = Statupdate("Rogue", "Love", R_Love, 90, -7)
            if Total_Cost >= 15:
                    $ R_Love = Statupdate("Rogue", "Love", R_Love, 200, -6)
                    if Party[0] == "Rogue" and Play_Cost > Prime_Cost:
                        $ R_Love = Statupdate("Rogue", "Love", R_Love, 200, -10)
                        $ R_Obed = Statupdate("Rogue", "Obed", R_Obed, 80, 4)
                    elif Party[1] == "Rogue" and Play_Cost > Second_Cost:
                        $ R_Love = Statupdate("Rogue", "Love", R_Love, 200, -10)
                        $ R_Obed = Statupdate("Rogue", "Obed", R_Obed, 80, 4)
            if ApprovalCheck("Rogue", 1100) and not Party[1]:
                    call RogueFace("sad")
                    ch_r "Well, ok, I guess I can cover it this time."
                    $ R_Obed = Statupdate("Rogue", "Obed", R_Obed, 30, 3)
                    $ R_Obed = Statupdate("Rogue", "Obed", R_Obed, 80, 2)   
                    if bg_current != "bg movies" and "dinnersex" in R_RecentActions:
                            call Date_Bonus("Rogue", -Total_Cost)
            elif ApprovalCheck("Rogue", 1300) and Party[1]:
                    call RogueFace("sad")
                    ch_r "Hm, ok, I guess I can cover it this time."
                    $ R_Love = Statupdate("Rogue", "Love", R_Love, 80, -5)
                    $ R_Obed = Statupdate("Rogue", "Obed", R_Obed, 30, 4)
                    $ R_Obed = Statupdate("Rogue", "Obed", R_Obed, 80, 3)    
                    if bg_current != "bg movies" and "dinnersex" in R_RecentActions:
                            call Date_Bonus("Rogue", -Total_Cost)
            else:                    
                    call RogueFace("angry")
                    if Party[1]:
                        $ R_Love = Statupdate("Rogue", "Love", R_Love, 80, -5)
                        ch_r "Oh, bullshit, I am NOT payin for her."
                    else:
                        ch_r "No way, you're coverin your own bills, [R_Petname]." 
                    if P_Cash >= Play_Cost: 
                        $ Line = "split"
                    else:
                        $ Line = "deadbeat" 
            #end asked Rogue to pay
                        
    elif Line == "Kitty":  
            #If you ask Kitty to pay
            $ K_Love = Statupdate("Kitty", "Love", K_Love, 90, -7)
            if Total_Cost >= 15:
                    $ K_Love = Statupdate("Kitty", "Love", K_Love, 200, -6)
                    if Party[0] == "Kitty" and Play_Cost > Prime_Cost:
                        $ K_Love = Statupdate("Kitty", "Love", K_Love, 200, -10)
                        $ K_Obed = Statupdate("Kitty", "Obed", K_Obed, 80, 4)
                    elif Party[1] == "Kitty" and Play_Cost > Second_Cost:
                        $ K_Love = Statupdate("Kitty", "Love", K_Love, 200, -10)
                        $ K_Obed = Statupdate("Kitty", "Obed", K_Obed, 80, 4)
            if ApprovalCheck("Kitty", 1000) and not Party[1]:
                    call KittyFace("sad")
                    ch_k "Huh? I mean I guess I can. . ."
                    $ K_Obed = Statupdate("Kitty", "Obed", K_Obed, 30, 3)
                    $ K_Obed = Statupdate("Kitty", "Obed", K_Obed, 80, 2)  
                    if bg_current != "bg movies" and "dinnersex" in K_RecentActions:
                            call Date_Bonus("Kitty", -Total_Cost)
            elif ApprovalCheck("Kitty", 1300) and Party[1]:
                    call KittyFace("sad")
                    ch_k "Huh? I mean I guess I can. . ."
                    $ K_Love = Statupdate("Kitty", "Love", K_Love, 80, -5)
                    $ K_Obed = Statupdate("Kitty", "Obed", K_Obed, 30, 4)
                    $ K_Obed = Statupdate("Kitty", "Obed", K_Obed, 80, 3)  
                    if bg_current != "bg movies" and "dinnersex" in K_RecentActions:
                            call Date_Bonus("Kitty", -Total_Cost)
            else:                    
                    call KittyFace("angry")
                    if Party[1]:
                        $ K_Love = Statupdate("Kitty", "Love", K_Love, 80, -5)
                        ch_k "You have GOT to be kidding! I'm not paying for her too!"
                    else:
                        ch_k "As if! You're paying for yourself, [K_Petname]." 
                    if P_Cash >= Play_Cost: 
                        $ Line = "split"
                    else:
                        $ Line = "deadbeat" 
            #end asked Kitty to pay                   
    
    elif Line == "Emma":  
            #If you ask Emma to pay
            $ E_Love = Statupdate("Emma", "Love", E_Love, 90, -3)
            if Total_Cost >= 15:
                    $ E_Love = Statupdate("Emma", "Love", E_Love, 200, -6)
                    if Party[0] == "Emma" and Play_Cost > Prime_Cost:
                        $ E_Love = Statupdate("Emma", "Love", E_Love, 200, -5)
                        $ E_Obed = Statupdate("Emma", "Obed", E_Obed, 80, 4)
                    elif Party[1] == "Emma" and Play_Cost > Second_Cost:
                        $ E_Love = Statupdate("Emma", "Love", E_Love, 200, -5)
                        $ E_Obed = Statupdate("Emma", "Obed", E_Obed, 80, 4)
            if ApprovalCheck("Emma", 900) and not Party[1]:
                    call EmmaFace("sad")
                    ch_e "I suppose you a student, after all. . ."
                    $ E_Obed = Statupdate("Emma", "Obed", E_Obed, 30, 3)
                    $ E_Obed = Statupdate("Emma", "Obed", E_Obed, 80, 2)     
                    if bg_current != "bg movies" and "dinnersex" in E_RecentActions:
                            call Date_Bonus("Emma", -Play_Cost)         
            elif ApprovalCheck("Emma", 1100) and Party[1]:
                    call EmmaFace("sad")
                    ch_e "I suppose you are students, after all. . ."
                    $ E_Love = Statupdate("Emma", "Love", E_Love, 80, -5)
                    $ E_Obed = Statupdate("Emma", "Obed", E_Obed, 30, 4)
                    $ E_Obed = Statupdate("Emma", "Obed", E_Obed, 80, 3)    
                    if bg_current != "bg movies" and "dinnersex" in E_RecentActions:
                            call Date_Bonus("Emma", -Play_Cost)           
            else:                    
                    call EmmaFace("angry")
                    if Party[1]:
                        $ E_Love = Statupdate("Emma", "Love", E_Love, 80, -5)
                        ch_e "I'm certainly not paying {i}her{/i} tab."
                    else:
                        ch_e "Student or not, I'm not paying your bills, [E_Petname]." 
                    if P_Cash >= Play_Cost: 
                        $ Line = "split"
                    else:
                        $ Line = "deadbeat"   
            #end asked Emma to pay         
                        
    if Line == "split": 
            #If you ask to split it evenly
            if "Rogue" in Party:
                    if ApprovalCheck("Rogue", 600):
                        call RogueFace("sad",Mouth="normal")
                        ch_r "Fine, I guess that's fair."
                        $ R_Obed = Statupdate("Rogue", "Obed", R_Obed, 50, 2)
                    else:
                        call RogueFace("angry",Eyes="side")
                        ch_r "Tch. Cheapskate."     
                        
                        if Party[0] == "Rogue" and Prime_Cost >=15:          
                            $ R_Love = Statupdate("Rogue", "Love", R_Love, 200, -5)
                        elif Party[1] == "Rogue" and Second_Cost >= 15:
                            $ R_Love = Statupdate("Rogue", "Love", R_Love, 200, -5)
                        else:
                            $ R_Love = Statupdate("Rogue", "Love", R_Love, 200, -3)
            if "Kitty" in Party:
                    if ApprovalCheck("Kitty", 600):
                        call KittyFace("sad",Mouth="normal")
                        ch_k "Yeah[K_like]ok."
                        $ K_Obed = Statupdate("Kitty", "Obed", K_Obed, 50, 2)
                    else:
                        call KittyFace("angry",Eyes="side")
                        ch_k "Jerk."       
                        
                        if Party[0] == "Kitty" and Prime_Cost >=15:          
                            $ K_Love = Statupdate("Kitty", "Love", K_Love, 200, -5)
                        elif Party[1] == "Kitty" and Second_Cost >= 15:
                            $ K_Love = Statupdate("Kitty", "Love", K_Love, 200, -5)
                        else:
                            $ K_Love = Statupdate("Kitty", "Love", K_Love, 200, -3)
            if "Emma" in Party:
                    if ApprovalCheck("Emma", 600):
                        call EmmaFace("sad",Mouth="normal")
                        ch_e "I suppose you are still on a student's budget."
                        $ E_Obed = Statupdate("Emma", "Obed", E_Obed, 50, 2)
                    else:
                        call EmmaFace("sad",Eyes="side")
                        ch_e "You should learn not to ask a woman out if you can't afford it." 
                        if Party[0] == "Emma" and Prime_Cost >=15:          
                            $ E_Love = Statupdate("Emma", "Love", E_Love, 200, -5)
                        elif Party[1] == "Emma" and Second_Cost >= 15:
                            $ E_Love = Statupdate("Emma", "Love", E_Love, 200, -5)
                        else:
                            $ E_Love = Statupdate("Emma", "Love", E_Love, 200, -3)
                            
            $ Prime_Bonus -= 10 if Prime_Cost >= 15 else 0
            $ Second_Bonus -= 10 if Second_Cost >= 15 else 0 
            $ P_Cash -= Play_Cost
            
    if Line == "deadbeat":  
            #If you cannot pay.
            $ Prime_Bonus -= Play_Cost
            $ Second_Bonus -= Play_Cost
            $ Prime_Bonus -= (Prime_Cost - 10) if Prime_Cost > 10 else 0
            $ Second_Bonus -= (Second_Cost - 10) if Second_Cost > 10 else 0
              
            if "Rogue" in Party:
                    if Party[0] == "Rogue" and Total_Cost >=15:          
                            $ R_Love = Statupdate("Rogue", "Love", R_Love, 200, -4)
                            if Play_Cost > Prime_Cost:
                                $ R_Love = Statupdate("Rogue", "Love", R_Love, 200, -10)
                    elif Party[1] == "Rogue" and Total_Cost >= 15:
                            $ R_Love = Statupdate("Rogue", "Love", R_Love, 200, -4)
                            if Play_Cost > Second_Cost:
                                $ R_Love = Statupdate("Rogue", "Love", R_Love, 200, -10)
                    if bg_current != "bg movies" and "dinnersex" in R_RecentActions:
                            call Date_Bonus("Rogue", -Total_Cost)
                    $ R_Obed = Statupdate("Rogue", "Obed", R_Obed, 50, -2)
                    
                    call RogueFace("sad")
                    
                    if ApprovalCheck("Rogue", 800):
                        ch_r "Aw, poor baby."      
                    else:
                        $ R_Brows = "angry"
                        ch_r "Well that's pretty weak, asking a girl out when you can't even afford it."
                        $ R_Love = Statupdate("Rogue", "Love", R_Love, 200, -3)
                        if "deadbeat" not in R_History:  
                            $ R_History.append("deadbeat") 
                        else:
                            call Rogue_Date_Over
            if "Kitty" in Party:
                    if Party[0] == "Kitty" and Total_Cost >=15:          
                            $ K_Love = Statupdate("Kitty", "Love", K_Love, 200, -4)
                            if Play_Cost > Prime_Cost:
                                $ K_Love = Statupdate("Kitty", "Love", K_Love, 200, -10)
                    elif Party[1] == "Kitty" and Total_Cost >= 15:
                            $ K_Love = Statupdate("Kitty", "Love", K_Love, 200, -4)
                            if Play_Cost > Second_Cost:
                                $ K_Love = Statupdate("Kitty", "Love", K_Love, 200, -10)
                                
                    if bg_current != "bg movies" and "dinnersex" in K_RecentActions:
                            call Date_Bonus("Kitty", -Total_Cost)
                    $ K_Obed = Statupdate("Kitty", "Obed", K_Obed, 50, -2)
                    
                    call KittyFace("sad")
                    
                    if ApprovalCheck("Kitty", 800):
                        ch_k "That's so[K_like]sad."         
                    else:
                        $ K_Brows = "angry"
                        ch_k "I wouldn't have gone out with you if I'd known you were such a bum." 
                        $ K_Love = Statupdate("Kitty", "Love", K_Love, 200, -3)
                        if "deadbeat" not in K_History:  
                            $ K_History.append("deadbeat") 
                        else:
                            call Kitty_Date_Over
                            
            if "Emma" in Party:
                    if Party[0] == "Emma" and Total_Cost >=15:          
                            $ E_Love = Statupdate("Emma", "Love", E_Love, 200, -4)
                            if Play_Cost > Prime_Cost:
                                $ E_Love = Statupdate("Emma", "Love", E_Love, 200, -5)
                                $ E_Obed = Statupdate("Emma", "Obed", E_Obed, 50, -2)
                    elif Party[1] == "Emma" and Total_Cost >= 15:
                            $ E_Love = Statupdate("Emma", "Love", E_Love, 200, -4)
                            if Play_Cost > Second_Cost:
                                $ E_Love = Statupdate("Emma", "Love", E_Love, 200, -5)
                                $ E_Obed = Statupdate("Emma", "Obed", E_Obed, 50, -2)
                    if bg_current != "bg movies" and "dinnersex" in E_RecentActions:
                            call Date_Bonus("Emma", -Total_Cost)
                    $ E_Obed = Statupdate("Emma", "Obed", E_Obed, 50, -2)
                    
                    call EmmaFace("sad")
                    
                    if ApprovalCheck("Emma", 800):
                        ch_e "Well that's just irresponsible."         
                    else:
                        $ E_Brows = "angry"
                        ch_e "You really should learn not to shop outside your class, [E_Petname]." 
                        $ E_Love = Statupdate("Emma", "Love", E_Love, 200, -3)
                        if "deadbeat" not in E_History:  
                            $ E_History.append("deadbeat") 
                        else:
                            call Emma_Date_Over
    #end choice consequences
    
    #Boosts lust based on price spent
    if Party[0] == "Rogue":
            $ R_Lust = Statupdate("Rogue", "Lust", R_Lust, 75, (Prime_Bonus/2))
    elif Party[1] == "Rogue":
                $ R_Lust = Statupdate("Rogue", "Lust", R_Lust, 75, (Second_Bonus/2))
    if Party[0] == "Kitty":
            $ K_Lust = Statupdate("Kitty", "Lust", K_Lust, 75, (Prime_Bonus/2))
    elif Party[1] == "Kitty":
                $ K_Lust = Statupdate("Kitty", "Lust", K_Lust, 75, (Second_Bonus/2))
    if Party[0] == "Emma":
            $ E_Lust = Statupdate("Emma", "Lust", E_Lust, 75, (Prime_Bonus/2))
    elif Party[1] == "Emma":
                $ E_Lust = Statupdate("Emma", "Lust", E_Lust, 75, (Second_Bonus/2))
                                
    $ Play_Cost = 0
    $ Prime_Cost = 0
    $ Second_Cost = 0
    return
#end payment   / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / 
 
label Date_Bonus(Girl=0, Amount=0):
    #This updates the prime value if the girl is prime, second if not.
    # call Date_Bonus("Rogue",5)
    if Party[0] == Girl:
                $ Prime_Bonus += Amount
    elif Party[1] == Girl:
                $ Second_Bonus += Amount
    return       
        
        
#Start Date End  / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / /
label Date_End:
    #The end of the date jumped to from any end of date
    if Current_Time == "Evening":
            #makes it night time
            call Wait(Outfit = 0)        
            
            $ bg_current = "bg date"    
            call Set_The_Scene(Dress=0) 
            if "movie" in P_RecentActions:
                "After the movie, you head back to the dorms."
            else:
                "After dinner, you head back to the dorms."   
    else:
            $ bg_current = "bg player"  
            call Set_The_Scene(Entry=1,Dress=0)  
    
    if Party[1]:
            #if there are two girls
            menu:
                "Who's room do you visit first?"
                "Rogue" if "Rogue" in Party:  
                    jump R_Date_End
                "Kitty" if "Kitty" in Party:
                    jump K_Date_End
                "Emma" if "Emma" in Party: #disable
                    jump E_Date_End  
                "Bring them both back to your room" if Party[1]:
                    jump P_Date_End
                "Neither, just head home alone": #disable     
                    call Date_Ditched
                    jump Date_Over           
          
    if Party[0] == "Rogue":       
            jump R_Date_End
    elif Party[0] == "Kitty":   
            jump K_Date_End
    elif Party[0] == "Emma":   
            jump E_Date_End  
    else:
            "You head back to your room." 

label Date_Over:    
    if Current_Time == "Evening":
            #makes it night time
            call Wait(Outfit = 0)
    $ bg_current = "bg player"
    call CleartheRoom("All",0,1)
    $ renpy.pop_call() 
    $ renpy.pop_call()   
    jump Player_Room

label P_Date_End:   
    #Called if you call them back to your room    
    $ bg_current = "bg player"
    if "Rogue" in Party:
        $ R_Loc = "bg player"
    if "Kitty" in Party:
        $ K_Loc = "bg player"
    if "Emma" in Party:
        $ E_Loc = "bg player"
    call Set_The_Scene(Dress=0)
    call Taboo_Level  
    if Party[1]:
        "You bring the girls to your own door."
    elif Party:
        "You bring [Party[0]] to your own door."
    if Party[1]:
            menu:
                "Who do you want to talk to?"
                "Rogue" if R_Loc == "bg player":
                    jump R_Date_End
                "Kitty" if K_Loc == "bg player":
                    jump K_Date_End
                "Emma" if E_Loc == "bg player":
                    jump E_Date_End
                "Go to Sleep" if not Party:
                    pass
    else:
                if R_Loc == "bg player":
                    jump R_Date_End
                if K_Loc == "bg player":
                    jump K_Date_End
                if E_Loc == "bg player":
                    jump E_Date_End
    jump Player_Room
    
#label Date_Outcome:
#    #assigns dated status based on outcomes
#    if Party[0] == "Rogue" and Prime_Bonus > 0:    
#            $ R_DailyActions.append("dated") 
#    elif Party[0] == "Kitty" and Prime_Bonus > 0:   
#            $ K_DailyActions.append("dated") 
#    elif Party[0] == "Emma" and Prime_Bonus > 0:   
#            $ E_DailyActions.append("dated") 
#    if Party[1] == "Rogue" and Second_Bonus > 0:    
#            $ R_DailyActions.append("dated") 
#    elif Party[1] == "Kitty" and Second_Bonus > 0:   
#            $ K_DailyActions.append("dated") 
#    elif Party[1] == "Emma" and Second_Bonus > 0:   
#            $ E_DailyActions.append("dated") 
#    return
            
label Date_Ditched(Girls=0):  
    #if you ditch out on a date, called by Date End
    #Girls tracks the number fo people who have already answered.
    if "Rogue" in Party: 
        if ApprovalCheck("Rogue", 1200):
            call RogueFace("confused")
            ch_r "Huh? Ok, bye, I guess."
        elif ApprovalCheck("Rogue", 400):
            call RogueFace("smile")
            ch_r "Oh, bye then."
        else:
            call RogueFace("angry")
            ch_r "Good riddance."
        $ R_Loc = "bg rogue"
        $ Girls += 1
    if "Kitty" in Party:
        if ApprovalCheck("Kitty", 1200):
            call KittyFace("confused")
            if Girls:
                ch_k "Yeah, um, bye?"
            else:
                ch_k "Um, bye?"
        elif ApprovalCheck("Kitty", 400):
            call KittyFace("smile")
            if Girls:
                ch_k "Yeah, Bye!"
            else:
                ch_k "Bye!"
        else:
            call KittyFace("angry")
            if Girls:
                ch_k "Yeah, later, asshole."
            else:
                ch_k "Later, asshole."
        $ K_Loc = "bg kitty"
        $ Girls += 1
    if "Emma" in Party:
        if ApprovalCheck("Emma", 1200):
            call EmmaFace("confused")
            if Girls:
                ch_e "Yes, a pity."
            else:
                ch_e "Oh? Pity"
        elif ApprovalCheck("Emma", 400):
            call EmmaFace("smile")
            if Girls:
                ch_e "Oh, yes, good night."
            else:
                ch_e "Good night then."
        else:
            call EmmaFace("angry")
            if Girls:
                ch_e "I'm not surprised."
            else:
                ch_e "You're excused!"
        $ E_Loc = "bg emma"
        $ Girls += 1
    
    return
        
        