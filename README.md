# CARMLS Hindi

This is a centralized repository of the work of the CARMLS research group on SNACS (Semantic Network of Adposition and Case Supersenses) for Hindi.

Currently, this includes the entire annotated *Nanhā Rājkumār* (*The Little Prince*) in Hindi.

Some open guidelines issues are stored (expectedly) as issues on the repo.

## Some differences from English STREUSLE annotations
1. All PRON lexcat gets SNACS annotation. Exceptions for nominative, wh-pronoun, oblique-case pronoun and unmarked reflexive pronouns, are created in PRON.NOM, PRON.WH, PRON.OBL and PRON.REFL exceptions. 
2. PRON lexcat skips validator check where MWE lexlemma must match MWE lemma, given some decisions around indexing the case marker in the lexlemma for irregular pronoun forms.
3. New PART.FOC lexcat for tokens with UD tag PART which get FOCUS annotations. Negative particles [nahin, na] get ADV lexcat. Other particles get PART lexcat.
4. Some MWE adpositions can't be validated using the lemma forms, as the tokens [ki, ke] seem to be lemmatized into [ka] but the MWE is always [ki tarah] or [ke/ki upar]. I haven't heard any case myself like [ka upar] or [ka tarah]. So MWE lexlemmas are validated against the raw token, instead of the lemma forms.
5. NONSNACS label has been removed.  
