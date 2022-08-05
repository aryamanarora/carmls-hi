# CARMLS Hindi

This is a centralized repository of the work of the CARMLS research group on SNACS (Semantic Network of Adposition and Case Supersenses) for Hindi.

Currently, this includes the entire annotated *Nanhā Rājkumār* (*The Little Prince*) in Hindi.

Some open guidelines issues are stored (expectedly) as issues on the repo.

## Some differences from English STREUSLE annotations
1. Irregular pronouns directly receive the SNACS label. This applies to genitive, dative, and accusative case forms. It's hard to find a theory to extract the genitive post-position from the irregular form.
2. 'Regular' pronouns which can be split into oblique form + post-position, have been re-tokenized into the two tokens, and SNACS label applied to the post-position. This includes case markers [ne, se, mem] and accusative/dative ko and genitive [ka,ke,ki] - basically when these markers are obvious in the morphology. 
3. New PART lexcat for tokens with UD tag PART. The exception is negative particles [nahin, na] which get ADV lexcat.
4. Some MWE adpositions can't be validated using the lemma forms, as the tokens [ki, ke] seem to be lemmatized into [ka] but the MWE is always [ki tarah] or [ke/ki upar]. I haven't heard any case myself like [ka upar] or [ka tarah]. So MWE lexlemmas are validated against the raw token, instead of the lemma forms.
5. NONSNACS label has been removed.  