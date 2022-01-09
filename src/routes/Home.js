import React, { useState } from "react";
import { Link } from "react-router-dom";
import { Container, Row, Col, Stack, Button, Card, Modal, Form } from "react-bootstrap";

function Home() {
    const [textarea, setTextarea] = useState(false);
    const [showImageModal, setShowImageModal] = useState(false);
    const [showMindMapModal, setShowMindMapModal] = useState(false);
    
    function openImageModal() {
        setShowImageModal(true);
    }

    function closeImageModal() {
        setShowImageModal(false);
        setTextarea(true);
    }

    function openMindMapModal() {
        setShowMindMapModal(true);
    }

    function closeMindMapModal() {
        setShowMindMapModal(false);
    }

    const [title, setTitle] = useState("");
    const [contents, setContents] = useState("");

    const onChangeTitle = (e) => {
        setTitle(e.target.value);
    };

    const onChangeContents = (e) => {
        setContents(e.target.value);
    }

    const onSubmit = (e) => {
        e.preventDefault();
        setTitle("");
    };

    return (
        <Container fluid>
            <Stack gap={3}>
                <Row>
                    <Col>
                        <Card>
                          <Card.Body>텍스트 요약 서비스</Card.Body>
                        </Card>
                    </Col>
                </Row>

                <Stack direction="horizontal" gap={1}>
                    <Button variant="outline-primary">텍스트 직접 입력</Button>
                    <Button variant="outline-secondary" onClick={openImageModal}>이미지 파일 업로드</Button>
                </Stack>

                <Modal
                    show={showImageModal}
                    onHide={closeImageModal}
                    dialogClassName="modal-90w"
                    aria-labelledby="example-custom-modal-styling-title"
                >
                    <Modal.Header closeButton>
                      <Modal.Title id="example-custom-modal-styling-title">
                        이미지 업로드
                      </Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <Form.Group controlId="formFile" className="mb-3">
                          <Form.Label>이미지 파일을 선택 해주세요.</Form.Label>
                          <Form.Control type="file" />
                        </Form.Group>
                    </Modal.Body>
                    <Modal.Footer>
                      <Button variant="primary" onClick={closeImageModal}>
                        텍스트 추출하기
                      </Button>
                    </Modal.Footer>
                </Modal>


                <Stack gap={0}>
                    <Row>
                        <Col sm={8}>
                            <Form onSubmit={onSubmit}>
                                <Form.Group className="mb-3" controlId="formBasicEmail">
                                  <Form.Label>제목</Form.Label>
                                  <Form.Control placeholder="제목을 입력해주세요." value={title} 
                                                  onChange={onChangeTitle}/>
                                </Form.Group>

                                <Form.Group className="mb-3" controlId="formBasicPassword">
                                  <Form.Label>요약할 내용</Form.Label>
                                  <Form.Control as="textarea" defaultValue={textarea? ("추출한 텍스트") : ("")}
                                                  onChange={onChangeContents}/>
                                </Form.Group>

                                <Button variant="primary" type="submit">
                                  요약하기
                                </Button>
                            </Form>
                        </Col>
                    </Row>  
                </Stack>

                <Row>
                    <Col sm={8}>
                        <Card border="dark">
                            <Card.Header>요약 결과</Card.Header>
                            <Card.Body>
                              <Card.Title>{title}</Card.Title>
                              <Card.Text>
                                {contents}
                              </Card.Text>
                            </Card.Body>
                        </Card>
                    </Col>
                </Row>

                <Row>
                    <Col md="auto">
                      <Link to="/quiz">
                          <Button variant="primary" size="md">
                            QUIZ
                          </Button>
                      </Link>
                    </Col> 
                    <Col md="auto">
                      <Button variant="secondary" size="md" onClick={openMindMapModal}>
                          마인드맵
                      </Button>
                    </Col>
                </Row>

                <Modal
                show={showMindMapModal}
                onHide={closeMindMapModal}
                dialogClassName="modal-90w"
                aria-labelledby="example-custom-modal-styling-title"
                >
                <Modal.Header closeButton>
                    <Modal.Title id="example-custom-modal-styling-title">
                      마인드맵
                    </Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <p>마인드맵 이미지</p>
                    </Modal.Body>
                </Modal>
            </Stack>
        </Container>
    );
}

export default Home;