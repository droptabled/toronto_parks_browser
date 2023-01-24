import React from 'react'

function Facility(props) {
  return (
    <a href={props.data.link}>
      <image src={props.data.imageLink} alt={props.data.altText} />
    </a>
  );
}

export default Facility;