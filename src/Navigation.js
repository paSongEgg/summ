import React, { useState } from "react";
import styled from "styled-components";
import SearchBar from "components/SearchBar";
import { IoIosMenu } from "react-icons/io";

function Navigation () {
    const [menu, setMenu] = useState(false);
    return (
        <Common>
            <HomeBox>
                <LogoImg src="img/island.svg"/>
                <Home href="/">SUMM</Home>
            </HomeBox>

            <MenuBox menu={menu}>
                <br></br>
                <Menu href="/">오늘의 뉴스</Menu>
                <Menu href="/sections">섹션별 뉴스</Menu>
                <SearchBar></SearchBar>
            </MenuBox>

            <Menubar href='#' onClick={() => {setMenu(!menu)}}>
                <IoIosMenu/>
            </Menubar>
        </Common>
    );
};

const Common = styled.div`
    display: flex;
    justify-content: space-around;
    margin: 20px;
    @media screen and (max-width: 550px) {
        flex-direction: column;
    }
`

const Home = styled.a`
    display: flex;
    align-items:center;
    font-size: 30px;
    margin 10px;
    text-decoration: none;
    color: black;
    font-weight: bold;
`
const LogoImg = styled.img`
    width:40px;
`
const HomeBox = styled.div`
    display: flex;
    align-items:center;
`

const MenuBox = styled.div`
    display: flex;
    align-items:center;
    @media screen and (max-width: 550px) {
        flex-direction: column;
        align-items:flex-end;
        display: ${({menu}) => {
           return menu === false ? 'none' : 'flex'
        }};
    }
`

const Menu = styled.a`
    margin: 10px;
    text-decoration: none;
    color: black;
`

const Menubar = styled.a`
    display: flex;
    align-items:center;
    font-size: 30px;
    position: absolute;
    right: 32px;
    height: 97px;
    @media screen and (min-width: 550px) {
        display: none;    
    }
`

export default Navigation;