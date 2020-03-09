import React, {Card} from 'react'



function Quote(props) {
  return (
    <Card style={{ width: '18rem' }}>
  <Card.Img height={200}  variant="top" src="https://www.placecage.com/200/300" />
  <Card.Body>
    <Card.Title>{props.quoter}</Card.Title>
    <Card.Text>
      {props.quote}
    </Card.Text>
  </Card.Body>
</Card>
  )
  return (<div>{props.quote}</div>)
}

export default Quote