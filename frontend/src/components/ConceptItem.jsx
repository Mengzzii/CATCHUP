import React from 'react'

const ConceptItem = ({concept, onClick}) => {


    return <div style={{
        display: "flex",
        padding: "2px",
        backgroundColor: "#FB6D6D",
        gap: "2px",
        borderRadius: "2px",
        marginTop: "1px", fontSize: "20px"}}
        onClick={onClick}
        >
        {concept}</div>

}

export default ConceptItem;