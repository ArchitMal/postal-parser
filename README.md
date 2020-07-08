# postal-parser
Probabilistic postal pyspark parser project pod.

### Tasks

- [x] Download OpenAddress data - beautiful csv
- [x] Determine data syntax for modelling - CoNLL, 1 doc / address, custom B-XXX and I-XXX tags.
- [ ] Create python skeleton for data pre-processing
- [ ] Create example .txt of cage, dict tuples
- [ ] take csv, process into dict suitable for OpenCage
- [ ] take OpenCage  dicts, process into typical address strings
- [ ] take address strings & dicts, process into CoNLL daddress strings & dicts, process into CoNLL doc

### CoNLL document

```
-DOCSTART- -X- -X- O

Alice NPP NPP B-House
McAlice NPP NPP I-House
123 NPP NPP B-Street
Main NPP NPP I-Street
Street NPP NPP I-Street
Toronto NPP NPP B-City
ON NPP NPP B-State
M4J NPP NPP B-Postcode
0A7 NPP NPP I-Postcode
Canada NPP NPP B-Country

-DOCTYPE- -X- -X- O

Bob NPP NPP B-House
Bobbert NPP NPP I-House
456 NPP NPP B-Street
Second NPP NPP I-Street
Ave NPP NPP I-Street
Vancouver NPP NPP B-City
British NPP NPP B-State
Columbia NPP NPP I-State
V3H0A7 NPP NPP B-Postcode

```


