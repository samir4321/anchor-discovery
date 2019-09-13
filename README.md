
anchor discovery
----

Discover an endpoint indicating the role of the user by using the information provided by grouping user flows. This information is based on the assumption that the role can be assumed fixed within a given 'user behavior group'

**hack anchor discovery**

*  Group user flows by a hash of the set of the tuples of 
`(endpoint accessed, response code)`. Call this a *flow hash*.

* Select as anchor that endpoint and JSON response key whose value is most constant within a flow hash and has the most variation across flow hashes.

