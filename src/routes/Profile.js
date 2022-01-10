import React, { Component } from "react";
import styles from "./Profile.module.css";

function Profile() {
  return (
    <div className={styles.container}>
      <a href="/user/logout" class={styles.logoutBtn}>
        로그아웃
      </a>
      <section className={styles.sectionBox}>
        <div>
          <h1>내 정보</h1>
        </div>
        <div className="profile">
          <img className={styles.profileImage} src="img/기본프로필.jpg" />
          <h3>userID</h3>
          <p>
            <span>userName</span>
          </p>
        </div>
      </section>

      <section className={styles.sectionBox}>
        <h2>내 계정</h2>
        <a href="/my/email" class={styles.item}>
          이메일 변경
        </a>
        <a href="/my/password" class={styles.item}>
          비밀번호 변경
        </a>
      </section>

      <section className={styles.sectionBox}>
        <h2>내 요약</h2>
        <a href="/my/summ" class={styles.item}>
          요약 기록
        </a>
        <a href="/my/quiz" class={styles.item}>
          퀴즈 기록
        </a>
        <a href="/my/quizresult" class={styles.item}>
          기타 내역..
        </a>
      </section>
    </div>
  );
}

export default Profile;
