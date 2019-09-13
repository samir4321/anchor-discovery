
anchor discovery
----



**hack anchor discovery**

*  Group user flows by a hash of the set of the tuples of 
`(endpoint accessed, response code)`. Call this a *flow hash*.

* Select as anchor that endpoint and JSON response key whose value is most constant within a flow hash and has the most variation across flow hashes.

