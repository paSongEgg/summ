import React, { Component } from "react";
import styles from "./Quiz.module.css";
import {
  Container,
  Row,
  Col,
  Stack,
  Button,
  Card,
  Modal,
  Form,
} from "react-bootstrap";

function Quiz() {
  return (
    <div>
      <div className={styles.container}>
        <div className={styles.sectionBox}>
          <div>
            <h1>퀴즈</h1>
          </div>
        </div>

        <div className={styles.sectionBox}>
          <h3>퀴즈 생성 위한 공간</h3>
          <p>//</p>
          <button type="button" class="btn btn-primary">
            퀴즈 생성하기
          </button>
          <button className={styles.createQuizBtn}>퀴즈 생성하기</button>
        </div>

        <div className={styles.sectionBox}>
          <div class="quizlist" className={styles.container}>
            <h3>지난 퀴즈</h3>
            <ul class="quiz-listing" className={styles.quizlisting}>
              <li class="quiz-listing-item" className={styles.quizItem}>
                <article class="prev quiz">
                  <header class="quiz-image">
                    <div class="quiz-image">
                      <img
                        className={styles.quizListImg}
                        src="img/sym02.gif"
                      ></img>
                    </div>
                    <a>제목</a>
                  </header>
                </article>
              </li>
              <li class="quiz-listing-item" className={styles.quizItem}>
                <article class="prev quiz">
                  <header class="quiz-image">
                    <div class="quiz-image">
                      <img
                        className={styles.quizListImg}
                        src="img/sym02.gif"
                      ></img>
                    </div>
                    <a>22/00/00 생성된 퀴즈</a>
                  </header>
                </article>
              </li>
              <li class="quiz-listing-item" className={styles.quizItem}>
                <article class="prev quiz">
                  <header class="quiz-image">
                    <div class="quiz-image">
                      <img
                        className={styles.quizListImg}
                        src="img/sym02.gif"
                      ></img>
                    </div>
                    <a>썸네일</a>
                  </header>
                </article>
              </li>
              <li class="quiz-listing-item" className={styles.quizItem}>
                <article class="prev quiz">
                  <header class="quiz-image">
                    <div class="quiz-image">
                      <img
                        className={styles.quizListImg}
                        src="img/sym02.gif"
                      ></img>
                    </div>
                    <a>ㅇㅇㅇ</a>
                  </header>
                </article>
              </li>
              <li class="quiz-listing-item" className={styles.quizItem}>
                <article class="prev quiz">
                  <header class="quiz-image">
                    <div class="quiz-image">
                      <img
                        className={styles.quizListImg}
                        src="img/sym02.gif"
                      ></img>
                    </div>
                    <a>ㄴㄴㄴㄴㄴ</a>
                  </header>
                </article>
              </li>
              <li class="quiz-listing-item" className={styles.quizItem}>
                <article class="prev quiz">
                  <header class="quiz-image">
                    <div class="quiz-image">
                      <img
                        className={styles.quizListImg}
                        src="img/sym02.gif"
                      ></img>
                    </div>
                    <a>퀴즈</a>
                  </header>
                </article>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Quiz;
