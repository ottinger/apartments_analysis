SELECT p.id AS id, p.propertyid AS propertyid, p.location AS location, p.subdivision AS subdivision, b.bldg_description AS bldg_description, b.year_built AS year_built, b.sq_ft AS sq_ft
	FROM realproperty AS p
	INNER JOIN (SELECT * FROM buildings) AS b ON p.id = b.local_property_id
	WHERE b.bldg_description IN ('Apartment <= 3 Stories', 'Condo <= 3 Stories', "Duplex One Story", "Duplex One half Story", "Duplex Two Story",
		"Multiple - Residential", "Triplex Multiple Story", "Triplex One Story", "Triplex One half Story", "Townhouse Multiple Story",
		"Townhouse One Story", "High-Rise Apartments")
	ORDER BY b.bldg_description

