import React from 'react';
import { css } from '@emotion/react';
import { useThemeContext } from '../contexts/ThemeContext';
import { ReactComponent as GithubIcon } from '../assets/github.svg';

const footerStyle = css`
  padding: 40px 16px;

  & > nav {
    margin: 0 auto;
    max-width: 1280px;
    display: flex;
    align-items: center;
    justify-content: space-between;

    svg {
      width: 2rem;
      height: 2rem;
    }
  }
`;

const iconStyle = (color) => css`
  width: 2rem;
  height: 2rem;
  stroke: ${color};
`;

const Footer = () => {
  const { isLight } = useThemeContext();

  return (
    <footer css={[footerStyle]}>
      <nav>
        <div>
          {new Date().getFullYear()} &copy; This project is licensed under the MIT License.
          <br />
          <br />
          <strong>Disclaimer:</strong> This project is for educational purposes only.
        </div>

        <div>
          <a href="https://github.com/AlphaeusNg/FYP" rel="noopener noreferrer" target="_blank">
            <GithubIcon css={iconStyle(isLight ? '#000' : '#fff')} className="github" />
          </a>
        </div>
      </nav>
    </footer>
  );
};

export default Footer;
