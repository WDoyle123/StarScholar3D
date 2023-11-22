SELECT TOP 10
    gaia_source.designation,
    gaia_source.source_id,
    gaia_source.ra,
    gaia_source.dec,
    gaia_source.parallax

WHERE 
    gaia_source.parallax > 7 AND gaia_source.parallax < 8 AND
    CONTAINS(
        POINT('ICRS', gaia_source.ra, gaia_source.dec),
        CIRCLE('ICRS', 37.954560666666666, 89.26410897222222, 0.016666666666666666)
    ) = 1;
