import React, { Component, useState, useEffect } from "react";
import { Link } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.css";
import axios from "axios";
import styles from "styles/Quiz.module.css";
import {
  Container,
  Row,
  Button,
  Pagination,
  Tabs,
  Tab,
  Spinner,
  Table,
} from "react-bootstrap";

function Quiz() {
  const [showing, setShowing] = useState(false);

  const [key, setKey] = useState("lastQuiz");

  let active = 2;
  let items = [];

  for (let number = 1; number <= 5; number++) {
    items.push(
      <Pagination.Item key={number} active={number === active}>
        {number}
      </Pagination.Item>
    );
  }

  return (
    <Container>
      <Row className="d-flex justify-content-center">
        <span className="mt-5 d-flex justify-content-center border">
          <h1>Quiz</h1>
        </span>

        <Row className="m-5 row-cols-1 d-flex justify-content-center">
          {showing ? (
            <Button
              variant="transparent"
              className="d-flex justify-content-center"
            >
              <Spinner
                as="span"
                animation="border"
                role="status"
                className="m-5"
              />
            </Button>
          ) : (
            <div className="mt-5 error row-cols-1 justify-content-center">
              <h1 className="mt-3 text-center">에러가 발생했습니다.</h1>
              <span className="mt-3 d-flex justify-content-center">
                <Button
                  onClick={fetchLastQuiz}
                  onClick={() => {
                    setShowing((showing) => !showing);
                  }}
                >
                  다시 불러오기
                </Button>
              </span>
            </div>
          )}
          <span className="m-3 d-flex justify-content-center">
            {!showing ? null : <Button variant="success">퀴즈 생성하기</Button>}
          </span>
        </Row>

        <Row className="m-3 d-flex row-cols-1 justify-content-center">
          <Tabs activeKey={key} onSelect={(k) => setKey(k)} className="mb-2">
            <Tab eventKey="lastQuiz" title="지난 퀴즈" onClick={onChange}>
              <Container>
                <Row className="list-group">
                  <a href="lastquiz" class="list-group-item bg-light">
                    지난 퀴즈 1
                  </a>
                  <a href="#" class="list-group-item bg-light">
                    지난 퀴즈 2
                  </a>
                  <a href="#" class="list-group-item bg-light">
                    지난 퀴즈 3
                  </a>
                  <a href="#" class="list-group-item bg-light">
                    지난 퀴즈 4
                  </a>
                  <a href="#" class="list-group-item bg-light">
                    지난 퀴즈 5
                  </a>
                </Row>

                <Table className="invisible">
                  <thead>
                    <tr>
                      <th>#</th>
                      <th>#</th>
                      <th>#</th>
                      <th>#</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td className="listId" th></td>
                      <td className="listQuizTitle" th></td>
                      <td className="listUserResult" th></td>
                    </tr>
                    {id !== 0 ? (
                      inputData.map(
                        (rowData) =>
                          // 최초 선언한 기본값은 나타내지 않음
                          rowData.id !== "" && (
                            <tr>
                              <td className="listId">
                                <Link to={`${rowData.id}`}>{rowData.id}</Link>
                              </td>
                              <td className="listQuizTitle">
                                <Link to={`${rowData.id}`}>
                                  {rowData.quizTitle}
                                </Link>
                              </td>
                              <td className="listUserResult">
                                <Link to={`${rowData.id}`}>
                                  {rowData.userResult}
                                </Link>
                              </td>
                            </tr>
                          )
                      )
                    ) : (
                      <tr>
                        <td className="listId"></td>
                        <td className="listQuizTitle noData">
                          작성된 글이 없습니다.
                        </td>
                        <td className="listUserResult noData"></td>
                      </tr>
                    )}
                  </tbody>
                </Table>
              </Container>
            </Tab>

            <Tab eventKey="wrong" title="오답">
              <Container>
                <Row className="list-group">
                  <a href="#" class="list-group-item bg-light">
                    오답 1
                  </a>
                  <a href="#" class="list-group-item bg-light">
                    오답 2
                  </a>
                  <a href="#" class="list-group-item bg-light">
                    오답 3
                  </a>
                  <a href="#" class="list-group-item bg-light">
                    오답 4
                  </a>
                  <a href="#" class="list-group-item bg-light">
                    오답 5
                  </a>
                </Row>
              </Container>
            </Tab>
          </Tabs>
        </Row>

        <Pagination className="m-3 d-flex justify-content-center">
          <Pagination.First tabindex="-1" />
          <Pagination.Prev />
          <Pagination.Item active>{1}</Pagination.Item>
          <Pagination.Item>{2}</Pagination.Item>
          <Pagination.Item>{3}</Pagination.Item>
          <Pagination.Item>{4}</Pagination.Item>
          <Pagination.Item>{5}</Pagination.Item>
          <Pagination.Next />
          <Pagination.Last />
        </Pagination>
      </Row>
    </Container>
  );
}

export default Quiz;
