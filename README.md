<h1>webSign</h1>

<h3><형상관리> - 각 branch 명과 역할</h3>
  <ui>
    <li>master - 배포를 위한 완성된 코드를 유지</li>
    <li>develop - 개발 통합을 위한 브랜치. feature 브랜치의 루트</li>
    <li>feature - 각 기능 개발을 위한 브랜치. f_(기능명)으로 브랜치를 작성</li>
  </ui>
<h3><진행사항></h3>
<ul>
  <li>
    2021-06-24
    <ul>
      <li>vue 환경설정 및 외부 라이브러리(vue-router, vuetify, vue-signaturepad) 설치</li>
    </ul>
  </li>
  <li>
    2021-06-25
    <ul>
      <li>MainLayout 컴포넌트 추가 - 관리자 페이지와 사용자 페이지에서 함께 사용될 공통 Layout </li>
      <li>Board 컴포넌트 추가 - 명단 정보 제공 및 서명 기능이 구현되어 있는 테이블 </li>
      <li>#1 Issue(v-dialog 스크롤 발생 현상) 해결</li>
      <li>vuetify icon "fontawesome" 에서 "mdi" 로 변경</li>
      <li>모바일 사이즈에서의 테이블 모양과 폰트사이즈 조정</li>
    </ul>
  </li>
  <li>
    2021-06-27
    <ul>
      <li>f_loadExcel - 엑셀파일 데이터 읽기 구현</li>
    </ul>
  </li>
   <li>
    2021-06-29
    <ul>
      <li>f_backEnd_Bill - Bill(인수증) CRUD API 구현</li>
    </ul>
  </li>
  </ul>
