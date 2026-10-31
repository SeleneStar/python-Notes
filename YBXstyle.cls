% MIT License
%
% Copyright (c) 2023 杨秉学
%
% Permission is hereby granted, free of charge, to any person obtaining a copy
% of this software and associated documentation files (the "Software"), to deal
% in the Software without restriction, including without limitation the rights
% to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
% copies of the Software, and to permit persons to whom the Software is
% furnished to do so, subject to the following conditions:
%
% 特此允许任何人免费获得本软件及相关文档文件(“软件”)的副本，
% 不受限制地处理本软件，包括但不限于其权利
% 使用、复制、修改、合并、出版、分发、再许可和/或出售 的拷贝本软件，
% 并允许本软件的所有者提供这样做，但须符合以下条件:
%
% The above copyright notice and this permission notice shall be included in all
% copies or substantial portions of the Software.
%
% 上述版权声明和本许可声明应包含在本软件的所有副本或主要部分中。
%
% THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
% IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
% FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
% AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
% LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
% OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
% SOFTWARE.
%
% 本软件是“按原样”提供的，没有任何形式的明示或明示的保证隐含的，
% 包括但不限于适销性保证;
% 适合某一特定目的和不侵权。在任何情况下都不得作者或版权所有者不承担任何索赔、损害赔偿或其他责任
% 在合同、侵权或其他诉讼中，因下列原因引起的责任:
%出于或与软件或使用或其他交易有关的%的软件。
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


% 命令\NeedsTeXFormat告诉编译器这个宏包是属于LaTeX的哪个版本的。
% 当前LaTeX的版本是LaTeX2e，几乎所有的发行版本都是用这个。
\NeedsTeXFormat{LaTeX2e}
% \ProvidesClass{} 自定义类
% 其他文档要是引用直接使用 \documentclass{YBXstyle}
\ProvidesClass{YBXstyle}

% changebar包允许沿着文本边缘的彩色条来设置示例和推导。
% 但是，它还在脚注旁边放了条，
% 这在这个类中是不希望出现的，
% 因此我们使用下面的实现了“撤消”该功能
\let\textbookcls@footnotetext\@footnotetext
\let\textbookcls@mpfootnotetext\@mpfootnotetext
\RequirePackage[leftbars,color,xcolor]{changebar}
\let\@footnotetext\textbookcls@footnotetext
\let\@mpfootnotetext\textbookcls@mpfootnotetext

% 这些选项需要进行一些修改才能实现，
% 因此我们声明一些新的 条件变量 来检查它们。
%%
%% 用 \newif 定义了一个 “ShortChapTitles” 的宏， 默认是False
%% \DeclareOption{ShortChapTitles} :
%%   当 ShortChapTitles 选项被指定时，\ShortChapTitles 宏的值将变为 true。
%% \ShortChapTitles 宏可以用于控制章节标题的长度。
\newif\ifShortChapTitles
\DeclareOption{ShortChapTitles}{
    \ShortChapTitlestrue
}

\newif\ifebook
\DeclareOption{ebook}{
    \ebooktrue
}

% Load the book class
% \PassOptionsToClass 宏用于将选项传递给另一个类。在本例中，它将 CurrentOption 宏的值传递给 ctexbook 类。
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{ctexbook}}
\ProcessOptions\relax

% \LoadClass[]{文章类型} 就是本class 是基于Latex提供的类
\ifebook
    \LoadClass[oneside,11pt]{ctexbook}
\else
    \LoadClass[letterpaper,11pt]{ctexbook}
\fi

% 字体设置
\RequirePackage{xeCJK} %调用系统中已安装的字体
\setCJKmainfont{SimSun} % 中文主要字体是仿宋
\setmainfont{Times New Roman} % 英文主要字体是Times New Roman
%% 支持汉字加粗
\let\heiti\relax % 黑体
\newCJKfontfamily\heiti{SimHei}[AutoFakeBold]
\setCJKsansfont{SimHei}[AutoFakeBold]

\let\songti\relax % 宋体
\newCJKfontfamily\songti{SimSun}[AutoFakeBold]
\setCJKmainfont{SimSun}[AutoFakeBold]

% 颜色设置
\definecolor{YBXPurple}{RGB}{102,8,116}
\definecolor{YBXGreen}{RGB}{0,166,82}
\definecolor{YBXRed}{RGB}{157,41,51}
\definecolor{NavyBlue}{RGB}{0, 0, 128}
\definecolor{YBXGrey}{RGB}{169,169,169}


% \RequirePackage[UTF8]{ctex}         %引入宏包
% \documentclass[UTF8]{ctexbook}      %设置文档类型
%
% 定义标题
% 需要注意的是，我们应该使用\RequirePackage而不是通常的\usepackage命令，
% 因为这是在一个类文件中。
% 即使在其他宏包使用同样的命令，\RequirePackage确保每个宏包被加载一次。
\RequirePackage[indentafter]{titlesec} % 设置标题格式
% [indentafter] 标题之后的段落都缩进
\RequirePackage{hyperref} % 提供了一些超链接功能
% 定义 subsubsubsection 命令
\titleclass{\subsubsubsection}{straight}[\subsection]
\newcounter{subsubsubsection}[subsubsection]
%\renewcommand\thesubsubsubsection{\thesubsubsection.\arabic{subsubsubsection}} % 编号样式 7.2.3.1 (前面7.2.3是\thesubsubsection的样式, . 是分隔符)
%\renewcommand\thesubsubsubsection{\Roman{subsubsubsection}}                    % 编号样式 [I]


%% 定义 subsubsubsection 标题格式
%\titleformat{\subsubsubsection}
%  {\color{YBXPurple}\heiti\raggedright\zihao{-4}\bfseries}{\thesubsubsubsection}{1em}{}
% 
\titleformat{\subsubsubsection}{\color{YBXPurple}\heiti\raggedright\zihao{-4}\bfseries}{[\Roman{subsubsubsection}]}{1em}{}
% 标题样式: 
%   颜色：YBXPurple
%   字体：黑体
%   对齐方式：左对齐
%   字号：-4
%   粗细：粗体
%   标题序号与标题内容间距：1em

% \titlespacing 用法：定义标题与上下段落的距离
% \titlespacing{command}{left spacing}{before spacing}{after spacing}[right]
\titlespacing*{\subsubsubsection}{0pt}{3.25ex plus 1ex minus .2ex}{1.5ex plus .2ex}


% 生成目录中要包含subsubsubsection、paragraph和subparagraph
% \makeatletter...\makeatother :
%   一些LATEX内部命令含有@字符,如\@startsection,如果需要在文档中使用这些内部命令,需要用\makeatletter...\makeatother包上
\makeatletter
\renewcommand\paragraph{\@startsection{paragraph}{5}{\z@}%
  {3.25ex \@plus1ex \@minus.2ex}%
  {-1em}%
  {\normalfont\normalsize\bfseries}}
\renewcommand\subparagraph{\@startsection{subparagraph}{6}{\parindent}%
  {3.25ex \@plus1ex \@minus .2ex}%
  {-1em}%
  {\normalfont\normalsize\bfseries}}
\def\toclevel@subsubsubsection{4}   % 定义了\subsubsubsection{}在生成目录时的级别是4
\def\toclevel@paragraph{5}          % 定义了\paragraph{}在生成目录时的级别是5
\def\toclevel@subparagraph{6}       % 定义了\subparagraph{}在生成目录时的级别是6
% 定义了\subsubsubsection{}在生成目录时的格式，使用4个点作为间隔，从第7em的位置开始，每个级别的跳距离是4em。
\def\l@subsubsubsection{\@dottedtocline{4}{10em}{4em}}
% 定义了\paragraph{}在生成目录时的格式，使用5个点作为间隔，从第10em的位置开始，每个级别的跳距离是5em
\def\l@paragraph{\@dottedtocline{5}{10em}{5em}}
% 定义了\subparagraph{}在生成目录时的格式，使用6个点作为间隔，从第14em的位置开始，每个级别的跳距离是6em。
\def\l@subparagraph{\@dottedtocline{6}{14em}{6em}}
\makeatother

\setcounter{secnumdepth}{5}
\setcounter{tocdepth}{5}

% \titleformat{\section}[left]{\normalfont\Large\bfseries}{\thesection}{1em}{}
% \titleformat{\subsection}[left]{\normalfont\Large\bfseries}{\thesubsection}{1em}{}
% \titleformat{\subsubsection}[left]{\normalfont\Large\bfseries}{\thesubsubsection}{1em}{}
% \titleformat{\subsubsubsection}[left]{\normalfont\Large\bfseries}{\thesubsubsubsection}{1em}{}
%
\ctexset{
    % 修改chapter
    chapter={
      name={第, 章},
      format += \color{YBXPurple}\heiti\centering\bfseries\Huge,
      number=\chinese{chapter},
      aftername=\hspace{0.2em},
      beforeskip=50pt, 
      afterskip=40pt
    },
  % 修改section
  section={
      name={,、},
      format=\color{YBXPurple}\heiti\raggedright\zihao{-3}\bfseries, % 设置 section标题为黑体、右对齐、小4号字
      number = \chinese{section}, % 编号为中文
      aftername=\hspace{1em},  % 标题和编号之间的距离
      beforeskip=1ex,          % 标题和上一段正文之间的距离
      afterskip=1ex          % 标题和下一段正文之间的距离
  },
  % 修改 subsection。
  subsection={
      name={,)},
      number={\arabic{subsection}},
      format=\color{YBXPurple}\heiti\raggedright\zihao{4}\bfseries, % 设置 subsection 标题为黑体、5号字
      aftername=\hspace{1em},
      beforeskip=1ex,
      afterskip=1ex
    },
   subsubsection={
      name={(,)},
      number={\arabic{subsubsection}},
      format=\color{YBXPurple}\heiti\raggedright\zihao{-4}\bfseries, % 设置 subsection 标题为黑体、5号字
      aftername=\hspace{1em},
      beforeskip=1ex,
      afterskip=1ex
    }%,
    %subsubsubsection={
    %   name={[,]},
    %   number={\arabic{subsection}},
    %   format=\color{YBXPurple}\heiti\raggedright\zihao{-4}, % 设置 subsection 标题为黑体、5号字
    %   aftername=\hspace{1pt},
    %   beforeskip=1ex,
    %   afterskip=1ex
    % }
}



% 添加首行缩进，两个字符
%\RequirePackage{indentfirst}
%\setlength{\parindent}{2em}

% 这个包允许我们在需要的时候调整页边距到页面中心。
\RequirePackage{changepage}
\RequirePackage{adjmulticol}
\newenvironment{FullWidth}[1][1]{\begin{adjmulticols}{#1}{0in}{-2in}}{\end{adjmulticols}}
% #1 #2 指的是传递到命令中的第一个和第二个参数。

% % 定义 chapter 标题格式
% \ifShortChapTitles
%   \renewcommand\@makechapterhead[1]{%
%   \begin{adjustwidth}{}{-2.25in}
%    \noindent{\parindent \z@ \raggedright \normalfont
%     \ifnum \c@secnumdepth >\m@ne
%       \if@mainmatter
%         \large\bfseries
%         \par\nobreak
%       \fi
%     \fi
%     \interlinepenalty\@M
%     \huge \bfseries \@chapapp\space \thechapter\\ \bigskip \LARGE #1\par\nobreak \medskip \hrule
%     \bigskip
%   }
%   \end{adjustwidth}
%   }
% \else
% \fi

%表格的包
\RequirePackage{tabularx}
\RequirePackage{multirow}

%\RequirePackage{framed}
%%% 制作方框 $> texdoc mdframed
\usepackage[framemethod=TikZ]{mdframed}
%%%% 定理的样式
\newcounter{Thm}[section]
%\renewcommand{\theThm}{\arabic{section}.\arabic{Thm}}
\newenvironment{Thm}[1][]{
	\refstepcounter{Thm}
	\mdfsetup{
		frametitle={
			\tikz[baseline=(current bounding box.east), outer sep=0pt]
			\node[anchor=east,rectangle,fill=blue!20]
      {\strut \ifstrempty{#1}{}{~#1}};},%Theorem~\theThm\ifstrempty{#1}{}{:~#1}};},
		innertopmargin=10pt,linecolor=blue!20,
		linewidth=2pt,topline=true,
		frametitleaboveskip=\dimexpr-\ht\strutbox\relax
	}
	\begin{mdframed}[]\relax
}{\end{mdframed}}

%%%% 定义的样式
\newcounter{Def}[section]
\newenvironment{Def}[1][]{
	\refstepcounter{Def}
	\mdfsetup{
		frametitle={
			\tikz[baseline=(current bounding box.east), outer sep=0pt]
			\node[anchor=east,rectangle,fill=orange!20]
      {\strut \ifstrempty{#1}{}{~#1}};},%Theorem~\theThm\ifstrempty{#1}{}{:~#1}};},
		innertopmargin=10pt,linecolor=orange!20,
		linewidth=2pt,topline=true,
		frametitleaboveskip=\dimexpr-\ht\strutbox\relax
	}
	\begin{mdframed}[]\relax
}{\end{mdframed}}

%%%% 定义
\newcounter{Tips}[section]
\newenvironment{Tips}[1][]{
	\refstepcounter{Tips}
	\mdfsetup{
		frametitle={
			\tikz[baseline=(current bounding box.east), outer sep=0pt]
			\node[anchor=east,rectangle,fill=violet!20]
      {\strut \ifstrempty{#1}{}{~#1}};},%Theorem~\theThm\ifstrempty{#1}{}{:~#1}};},
		innertopmargin=10pt,linecolor=violet!20,
		linewidth=2pt,topline=true,
		frametitleaboveskip=\dimexpr-\ht\strutbox\relax
	}
	\begin{mdframed}[]\relax
}{\end{mdframed}}

% %%%% 词汇
% % \RequirePackage{fontspec}
\RequirePackage{tcolorbox}
\tcbuselibrary{skins,breakable} % 使用tcolorbox的皮肤和自动换页
\newtcolorbox[auto counter]{wordbox}[1][]{
  breakable,%自动换页
  colframe=green!50!white,%边框颜色
  coltitle=blue!50!red,%title颜色
  colback=yellow!10!white,%背景颜色
  fonttitle=\bfseries,%title字体
  title=\thetcbcounter.~#1, % 自动编号
%   title=#1, % 不编号
  subtitle style={boxrule=0.4pt,colback=blue!50!red!20},%子title样式
  before=,
}   
% \newtcolorbox[auto counter]{columnword}[1][]{
%   breakable, % 自动换页
%   colframe=green!50!white, % 边框颜色
%   coltitle=blue!50!red, % title颜色
%   colback=yellow!10!white, % 背景颜色
%   fonttitle=\bfseries, % title字体
%   title=\thetcbcounter.~#1,
%   subtitle style={boxrule=0.4pt,colback=blue!50!red!20}, % 子title样式
%   before=,
%   margin, % 将盒子放在页边
% }
% \RequirePackage{marginfix} % 修复marginpar的问题
\RequirePackage{marginnote} % 修复marginpar的问题
% marginnote 与 marginfix 的区别
% marginnote 会在页面的最底部插入一个空白页，而 marginfix 不会
% marginfix 如果页面的最底部没有足够的空间，会将 marginpar 移动到下一页
% \columnwordbox[allure]{n.吸引力，诱惑力=attractive=fascinating \\ v.吸引，引诱=tempt=attract}
\newtcolorbox{columnword}[1][]{
  enhanced,
  breakable, % 自动换页
  colframe=green!50!white, % 边框颜色
  coltitle=blue!50!red, % title颜色
  colback=yellow!10!white, % 背景颜色
  fonttitle=\bfseries, % title字体
  title=#1,
  subtitle style={boxrule=0.4pt,colback=blue!50!red!20}, % 子title样式
  overlay unbroken and first={
    \node[anchor=north east,inner sep=0pt,outer sep=0pt] at (frame.north east) {\tcbtitle};
  },
  before upper=\vspace*{-\baselineskip}, % 在上方添加负值的垂直空间
  remember as=mybox,
  top=15pt, % 设置上边距
  bottom=2pt, % 设置下边距
}

\newcommand{\columnwordbox}[2][]{%
  \marginpar{%
    \begin{columnword}[#1]
      #2
    \end{columnword}
  }
}

% 不要在 tabular 环境中使用 \columnwordfoot
\newcounter{columnwordfoot}
\newtcolorbox{columnwordfootbox}[2][]{
  enhanced,
  breakable, % 自动换页
  colframe=green!50!white, % 边框颜色
  coltitle=blue!50!red, % title颜色
  colback=yellow!10!white, % 背景颜色
  fonttitle=\bfseries, % title字体
  title=\thecolumnwordfoot. #2, % 在title前添加编号
  subtitle style={boxrule=0.4pt,colback=blue!50!red!20}, % 子title样式
  overlay unbroken and first={
    \node[anchor=north east,inner sep=0pt,outer sep=0pt] at (frame.north east) {\tcbtitle};
  },
  before upper=\vspace*{-\baselineskip}, % 在上方添加负值的垂直空间
  remember as=mybox,
  top=15pt, % 设置上边距
  bottom=2pt, % 设置下边距
}

\newcommand{\columnwordfoot}[3][]{%
  \textcolor{#1}{#2} % 设置原文中的颜色
  \refstepcounter{columnwordfoot}%
  \textcolor{#1}{\textsuperscript{\hyperlink{columnwordfoot.\thecolumnwordfoot}{\thecolumnwordfoot}}}%  // 设置超链接的颜色
  \marginpar{%
    \hypertarget{columnwordfoot.\thecolumnwordfoot}{}%
    \begin{columnwordfootbox}[#1]{#2}
      #3
    \end{columnwordfootbox}
  }
}

% 下面的包保证了图片可以插在正确的页边内
\RequirePackage{mparhack}

% 插入pdf
\RequirePackage{pdfpages}
\RequirePackage{pdflscape} % 横向排版

% % Set document font to be Utopia
%     %\RequirePackage[T1]{fontenc}
\RequirePackage{helvet} % 使用Helvetica字体
\RequirePackage{fourier} % 使用Utopia字体 使用\lefthand，但是Latex2023之前的版本不支持
% \RequirePackage{fourier-otf} % 使用Utopia字体
\RequirePackage{microtype} % 微调字体
% \RequirePackage{tipa} % 提供国际音标
%
% 增强数学公式效果
\RequirePackage{amsmath}
\RequirePackage{amsthm}  %输出\qedsymbol一个方框，在极限的时候使用
\RequirePackage{amssymb} % 输出 \because 和 \therefore
\RequirePackage{mathtools} % 数学工具包包括amsmath的扩展
\RequirePackage{mathrsfs} % 支持在数学中使用 Raph Smith’s Formal Script 字体。提供 \mathscr 命令，而不是像 calrsfs 中那样覆盖标准 \mathcal 命令。
\RequirePackage{bbm}      % 计算机现代字体的黑板变体。
\RequirePackage{esint}    % 打出高斯公式的 环路积分符号
\RequirePackage{empheq}   % 多行公式以及公式添加底色
\RequirePackage{extarrows} % 在等号XY上输入文字
\RequirePackage{chemarrow} % 在等号上输入文字扩展

% 文本高亮
\RequirePackage{soul} 
\newcommand{\mathcolorbox}[2]{\colorbox{#1}{$\displaystyle #2$}} % 数学公式高亮
% 段内代码
% \codeinline{Hello}
\definecolor{inlineBG}{HTML}{F1F1F1} % 段内代码背景色
\definecolor{inlineFG}{HTML}{FFC0CB} % 段内代码字体色
\newcommand{\codeinline}[1]{{%
  \sethlcolor{inlineBG}%
  \color{inlineFG}%
  \ttfamily
  \hl{\mbox{#1}}%
}}

%\sethlcolor{yellow}\hl{这里的内容会被高亮为黄色\cite{xxx}}
%\sethlcolor{pink}\hl{这里的内容会被高亮为粉色}
%\hl{这里的内容会被高亮为粉色} % 没有设置颜色的话，沿用上一次的设置
%\sethlcolor{yellow}\hl{这里的内容会被高亮为黄色}
% 中文高亮
% 用法：\cjkhl{ColorName}{高亮文本}
%       \cjkhl{ColorName}{高亮文本\textcolor{YBXPurple}{需要特殊标记的颜色}，其余内容}
% 不能里面使用$$数学公式
% 如果真的需要使用数学公式
% \cjkhl{yellow}{这个一个}\colorbox{yellow}{\color{black}$d_k=-[H(x_k)+\lambda_kI]^{-1}g(x_k)$}\cjkhl{yellow}{。和文本高亮，\textcolor{YBXPurple}{紫色问题}，}
\newcommand*{\cjkhl}[2]{{\def\xcjklhcolorbox{\colorbox{#1}}\xcjkhl#2\relax}}
% 定义了一个新命令\cjkhl，它接受2个参数
% \xcjklhcolorbox 表示一个接收颜色的\colorbox{ColorName}命令
% \xcjkhl 是一个递归的宏，它将文本分解为单个字符，并将每个字符放入一个颜色框中。
% \relax 表示结束递归

\makeatletter

%look ahhead for the next character
% \xcjkhl 递归的宏，它将文本分解为单个字符，并将每个字符放入一个颜色框中。
% \def 表示定义一个宏
% \futurelet 用于查看下一个字符，但不会消耗它
% \tmp 是一个临时变量，用于存储下一个字符
% \xxcjkhl 是一个递归的宏，它将文本分解为单个字符，并将每个字符放入一个颜色框中。
\def\xcjkhl{\futurelet\tmp\xxcjkhl}

% \xcjkhlleaders 帮助宏，用于创建带有高亮框的引导线。
\def\xcjkhlleaders{\leavevmode\leaders\hbox{%
  \fboxsep\z@\xcjklhcolorbox{\strut\kern.1pt%
  \ifx\cjkhlbleed\@empty\else\kern\cjkhlbleed\fi\relax}%
\ifx\cjkhlbleed\@empty\else\kern-\cjkhlbleed\fi\relax}}

% leaders with a 1pt of stretch/shrink to put before or after punctuation
\def\@@yhlstretch{\leavevmode\xcjkhlleaders\hskip\z@\@plus.1em \@minus.1em }

\def\@chkhlpar#1\fi\fi#2{\par\noindent\xcjkhl}

\def\@cjkhl@beforeafter#1{%
  \ifx\tmp#1%
    \@@yhlstretch
    \let\@chkhlstretch\@@yhlstretch
    \let\cjkhlpenalty\@highpenalty
  \fi}

\def\@cjkhl@after#1{%
  \ifx\tmp#1%
    \let\@chkhlstretch\@@yhlstretch
    \let\cjkhlpenalty\@highpenalty
  \fi}

\def\@cjkhl@before#1{%
  \ifx\tmp#1%
    \@@yhlstretch
    \let\cjkhlpenalty\@highpenalty
  \fi}

\def\xxcjkhl{%
%look for a \par (from \obeylines)
\ifx\tmp\par\expandafter\@chkhlpar\fi
%look for a \relax to finish
\ifx\tmp\relax
\else
%by default do no stretch leaders after the character
\let\@chkhlstretch\relax
\let\cjkhlpenalty\z@
%these stretch before and after
\@cjkhl@beforeafter？%
\@cjkhl@beforeafter；%
% these stretch after
\@cjkhl@after，%
\@cjkhl@after。%
\@cjkhl@after）%
\@cjkhl@after》%
\@cjkhl@after”%
%these stretch before
\@cjkhl@before（%
\@cjkhl@before《%
\@cjkhl@before“%
% look for a space
\ifx\tmp\@sptoken
\xxxcjkhlsp
\else
%default case stick the current character in a box
\xxxcjkhl
\fi\fi}

%make a highlight leaders stretch/shrink as much as a normal word space.
\def\xxxcjkhlsp#1\fi\fi#2{%
\fi\fi
\xcjkhlleaders\hskip \fontdimen2\font  plus \fontdimen3\font minus \fontdimen4\font\relax
\xcjkhl#2}

%get out of a double \if test
\def\xxxcjkhl\fi\fi{%
\fi\fi
\@chkhl}

%The simple case box the current character and start looking for the next.
% bleed slightly on the right to avoid gaps showing
\let\cjkhlbleed\@empty

% 在\cjkhl{}环境里面使用不能使用\textcolor
% \def\@chkhl#1{{%
% \fboxsep\z@
% \leavevmode\penalty\cjkhlpenalty
%   \xcjklhcolorbox{%
%    \strut#1\ifx\cjkhlbleed\@empty\else\kern\cjkhlbleed\fi}}%
% \ifx\cjkhlbleed\@empty\else\kern-\cjkhlbleed\fi\relax
% \@chkhlstretch
% \xcjkhl}%

% 修改这里，使得可以在\cjkhl{}环境里面使用\textcolor
\def\@chkhl#1{%
\ifx\textcolor#1% 如果参数以\textcolor开始
\let\next\@chkhltextcolor% 使用特殊的处理方式
\else% 否则像以前一样处理参数
\let\next\@chkhldefault% 使用默认的处理方式
\fi
\next#1}

% 处理\textcolor命令的宏
\def\@chkhltextcolor#1#2#3{%
#1{#2}{\cjkhl{yellow}{#3}}% 在\textcolor的参数中添加\cjkhl命令
\xcjkhl}

% 默认的处理方式
\def\@chkhldefault#1{%
{\fboxsep\z@
\leavevmode\penalty\cjkhlpenalty
\xcjklhcolorbox{%
\strut#1\ifx\cjkhlbleed\@empty\else\kern\cjkhlbleed\fi}}%
\ifx\cjkhlbleed\@empty\else\kern-\cjkhlbleed\fi\relax
\@chkhlstretch
\xcjkhl}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 允许命令使字体相对于当前更小
\RequirePackage{relsize}

% 包含插图
\RequirePackage{graphicx}
\RequirePackage{tikz}
\RequirePackage{pgfplots} % 引入axis环境

% 设置美国信纸的页边距
\setlength{\marginparwidth}{2in}
\setlength{\marginparsep}{0.25in}
\setlength{\oddsidemargin}{0.0in}
\setlength{\evensidemargin}{1.5in}
\setlength{\textwidth}{5in}
\setlength{\topmargin}{0in}
\setlength{\headheight}{0.2in}
\setlength{\headsep}{0.35in}
\setlength{\textheight}{8.4in}
\setlength{\footskip}{0.35in}
\setlength{\columnsep}{0.35in}
\raggedbottom
\renewcommand{\baselinestretch}{1}


% 页眉页脚
    \RequirePackage{calc}
    \RequirePackage{fancyhdr}
      \fancyhf{}
      \pagestyle{fancy}
      \fancyheadoffset[LE,RO]{\marginparsep+\marginparwidth}
      \fancyhead[LE,RO]{\bfseries\thepage}
      \fancyhead[LO]{\bfseries\rightmark}
      \fancyhead[RE]{\bfseries\leftmark}
      \fancyfoot[LO,RE]{}
      % E	偶数页
      % O 	奇数页
      % L	页眉或页脚的左边部分
      % C	页眉或页脚的中间部分
      % R	页眉或页脚的右边部分
      % H	页眉
      % F	页脚
      %\renewcommand{\chaptermark}[1]{\markboth{\chaptername \ \thechapter \ \ #1}{}} % 英文章名
      \renewcommand{\chaptermark}[1]{\markboth{第\ \chinese{chapter} \ 章\ #1}{}}
      %\renewcommand{\sectionmark}[1]{\markright{\thesection \ \ #1}}  % 英文节名
      \renewcommand{\sectionmark}[1]{\markright{\chinese{section}、\ #1}}

      % Index页面的风格
      \fancypagestyle{index}{%
      \fancyheadoffset[LE,RO]{1in}
      \fancyhead[LE,RO]{\bfseries\thepage}
      \fancyhead[LO,RE]{\bfseries\rightmark}
    }

% 这些命令修改TOC中留给页码的空间
     \makeatletter
     \renewcommand{\@pnumwidth}{2em}
     \renewcommand{\@tocrmarg}{2.85em}
     \makeatother

% Redefine double page clear to make it a blank page without headers
    \makeatletter
    \def\cleardoublepage{\clearpage\if@twoside \ifodd\c@page\else
    \hbox{}
    \thispagestyle{empty}
    \newpage
    \if@twocolumn\hbox{}\newpage\fi\fi\fi}
    \makeatother

% Allow more liberal figure placement
    \renewcommand{\topfraction}{0.9}	% max fraction of floats at top
    \renewcommand{\bottomfraction}{0.8}	% max fraction of floats at bottom
    \setcounter{topnumber}{2}
    \setcounter{bottomnumber}{2}
    \setcounter{totalnumber}{4}     % 2 may work better
    \setcounter{dbltopnumber}{2}    % for 2-column pages
    \renewcommand{\dbltopfraction}{0.9}	% fit big float above 2-col. text
    \renewcommand{\textfraction}{0.07}	% allow minimal text w. figs

% Enhanced raggedright for captions and tables
    \RequirePackage{ragged2e}
    % 长表格
    \RequirePackage{longtable}

% caption 评论样式
\RequirePackage[labelfont=bf,labelsep=none,justification=RaggedRight]{caption}
\DeclareCaptionFormat{suggested}{{\small #1#2 #3}}
\captionsetup{format=suggested}

% Automatically add section headings to index if the optional
% argument index is present.
\RequirePackage{xstring}
\newcommand{\indexedSection}[1]{\section{#1}
\IfBeginWith{#1}{The }{\StrBehind{#1}{The }[\Front]\index{\Front , The@\textbf{\Front , The}} }{\index{#1@\textbf{#1}} }
    }

% Make the index
\RequirePackage{makeidx}
\makeindex

% Allow per-chapter appendices
\RequirePackage[title,titletoc]{appendix}

\RequirePackage{ifthen}

% Add linking capability
%\RequirePackage[pdfpagemode=UseOutlines,
%            bookmarksnumbered,pdfpagelabels=true,plainpages=false,pdfstartview=FitH,
%            colorlinks=true,linkcolor=black,citecolor=black,urlcolor=blue]{hyperref}

%\RequirePackage{hyperref}
\hypersetup{
        pdftitle={Fundamentos de C\'alculo},
        pdfsubject={C\'alculo diferencial},
        bookmarksnumbered=true,
        bookmarksopen=true,
        bookmarksopenlevel=1,
        plainpages=false,
        colorlinks=true,
        pdfpagelabels=true,
        citecolor=black,
        filecolor=black,
        linkcolor=black,
        urlcolor=blue,
        pdfstartview=Fit,
        pdfpagemode=UseOutlines,
        pdfpagelayout=TwoPageRight
    }
\urlstyle{rm}


% Define the margin figure command
\RequirePackage{array}
\makeatletter
\def\maxwidth#1{\ifdim\Gin@nat@width>#1 #1\else\Gin@nat@width\fi}
\makeatother

\newcommand{\marginfig}[3][0pt]{
    \ifebook % Margin figures get shifted inline for ebooks.
        \par\bigskip\captionsetup{type=figure}
        \begin{center}\begin{tabular}{m{2in}m{2in}}
        \raisebox{-\height}{\includegraphics[width=2in]{#2}}
          &
          \vfill
        \captionof{figure}[]{#3} \label{#2}
         \vfill
          \\
        \end{tabular}\end{center}
        \bigskip\par
    \else
        \marginpar{\vskip#1 \captionsetup{type=figure}
        \vtop{\vskip0pt\hbox{\includegraphics[width=\maxwidth{2in}]{#2}}}
        \captionof{figure}[]{#3} \label{#2}}
    \fi}

% 定义 inlinefig(行内图片) 命令
% \newcommand{命令的名称}[参数个数]{定义内容}
% \newcommand{命令的名称}[参数个数][参数1的默认值]{定义内容}
% 下面的[3]表示有3个参数，但是其中 第一个参数 4.35in 已经给出了
% 所以只写后面两个参数也可以
\newcommand{\inlinefig}[3][4.35in]{
    \par \vspace{4pt}\parbox{4.35in}{
    \captionsetup{type=figure}
    \centering \includegraphics[width=#1]{#2}\par\vspace{0.03in}
    \captionof{figure}[hptb]{#3 \label{#2}} } \par \vspace{4pt}
}

% Define inneralign command
\strictpagecheck % Use if errors crop up
\newcommand{\side}{l}
\newcommand{\inneralign}[1]{
    \checkoddpage
    \ifoddpage
    \renewcommand{\side}{l}
    \else
    \renewcommand{\side}{r}
    \fi
    \noindent\makebox[\textwidth][\side]{#1}\par % 其中 \side 根据当前页是奇数页还是偶数页决定图片的对齐方式（左对齐或右对齐）
    % \noindent\makebox[\textwidth][c]{#1}\par
    }


% 定义 页边笔记提醒(margin note reminders)
% 3个参数，第一个是可选参数，表示页边距离，第二个是提醒内容，第三个是提醒内容

\newcommand{\reminder}[3][0pt]{
    \marginpar{\vskip #1
    \begin{enumerate}
        \item[#2] \small \RaggedRight 
        #3
    \end{enumerate}
    }
}

% 代码环境——Verbatim
%% 抄录长代码环境
\RequirePackage{upquote}
\RequirePackage{fancyvrb} % fancyvrb 宏包提供了高度可配置的抄录环境，功能大致上和 listings 相当
\RecustomVerbatimEnvironment
  {Verbatim}{Verbatim}{xleftmargin=0.25in,fontsize=\small}

\definecolor{DarkGreen}{rgb}{.133,.545,.133}
\definecolor{purple}{rgb}{0.625,0.125,0.9375}
\RequirePackage{listings}
\lstset{
    upquote=true,
    keepspaces=true,
    aboveskip=0in,
    belowskip=0.2in,
    language=C,
    fancyvrb=true,
    breaklines=true,
    basicstyle=\footnotesize\ttfamily,
    keywordstyle=\color{blue},        % 关键字样式
    %identifierstyle=\color{blue},        % 标识符样式
    commentstyle=\color{DarkGreen},     % 注释样式
    %mathescape=true, % 允许在注释中使用LaTeX数学公式 
    stringstyle=\ttfamily\color{violet},   % 字符串样式
    columns=fullflexible,
    numbers=left,
    numberstyle=\color{gray},
    stepnumber=1,                          % 行号递增1
    xleftmargin=1em,                       % 左空白1em
    tabsize=4,                             % tab等效空格数
    breaklines=true,                       % 自动断行
    breakatwhitespace=true,                % 只在空白位置断行
    showspaces=false,                      % 显式空格
    showstringspaces=false}

\newcommand{\listingFile}{none}

\newcounter{listingCtr}[chapter] % 定义计数器 listingCtr ，每一章(chapter)都会重置
\renewcommand{\thelistingCtr}{\arabic{chapter}.\arabic{listingCtr}}

%%%%%%%%%%%%%%%%%%%%%
% 如果使用pdfLaTeX编译，需要使用下面的代码
\RequirePackage{ifpdf}
\ifpdf
%This is needed to keep unique links for hyperref 以保持超链接的唯一性
\renewcommand{\theHlistingCtr}{\arabic{chapter}.\arabic{listingCtr}}
\fi
%%%%%%%%%%%%%%%%%%%%%

\newenvironment{codeexample}[1][] % 定义 codeexample 环境
{
    % 下面的代码就是判断是否有参数传入，
    % 如果有就使用传入的参数(就是文件名)，
    % 如果没有就使用默认的参数(文件名就是 ch<章节>ex<第几个listingCtr>.c)
    \par
    \refstepcounter{listingCtr}
    \ifthenelse{\equal{#1}{}}
    {
        \renewcommand{\listingFile}{ch\thechapter ex\arabic{listingCtr}.c}
    }
    {
        \renewcommand{\listingFile}{#1}
    }
}
{
    \lstinputlisting[escapeinside={(*@}{@*)},caption=(\listingFile),frame=TB]{\listingFile}
}

% 代码中插入公式
% \begin{codeexample}[problem-spec.h]
% \begin{VerbatimOut}{\listingFile}
% /*
%  * problem-spec.h
%  *  问题描述
%  *  ---------------
%  *  | (*@$\textcolor{DarkGreen}{\nabla\cdot(\eta(x,y)\nabla u(x,y)) + f(x,y) = \theta , (x,y)\in\Omega}$@*)
%  *  | (*@$\textcolor{DarkGreen}{u=g,(x,y)\in\Gamma_D(\partial\Omega_D)}$@*)
%  *  ---------------
%  */
% \end{VerbatimOut}
% \end{codeexample}
%% 定义多种风格的代码环境
\definecolor{verylightgray}{rgb}{.97,.97,.97}
\definecolor{Beige}{RGB}{245,245,220}
\lstdefinestyle{demostyle}{  
    language=Bash,  
    breaklines=true,                        % 自动将长的代码行换行排版  
    keywordstyle=\color{green}\bfseries,    % 设置关键字为粗体，颜色为绿色  
    deletekeywords={do, if, else, then, select, case, \#, for, in},      % 删除关键字，不显示do, if, else, \#等
    commentstyle=\color{blue} \textit,      % 注释样式，颜色为蓝色，斜体  
    showstringspaces=false,                 % 不显示字符串中的空格  
    numbers=none,                           % 不显示行号  
    frame=single,                           % 代码框为单线框  
    rulecolor=\color[rgb]{0.8,0.8,0.8},     % 设置代码框颜色  
    backgroundcolor=\color[rgb]{0.96,0.96,0.96},% 背景颜色  
    aboveskip=1em,                          % 代码框与上方文本之间的距离  
    belowskip=1em                           % 代码框与下方文本之间的距离  
}  
\lstdefinestyle{Cstyle}{
    language=C,
    backgroundcolor=\color{Beige},      % 背景颜色为 Beige
    breaklines=true,                    % 自动将长的代码行换行排版
    frame=single,                       % 代码框为单线框    
    numbers=left,                       % 行号显示在左侧
    numberstyle=\color{verylightgray},  % 行号颜色为浅灰色
    numberstyle=\small,                  % 行号字体为小号    
    stepnumber=1,                          % 行号递增1
    framesep=2em,                       % 设置边框(single)与代码的距离
    basicstyle=\ttfamily,               % 设置代码字体为等宽字体
    breaklines=true,                    % 自动换行
    keywordstyle=\bfseries\color{NavyBlue}, % 设置关键字为粗体，颜色为 NavyBlue
    keywordstyle=\color{blue},          % 关键字样式
    %identifierstyle=\color{doc},        % 标识符样式
    commentstyle=\color{DarkGreen},         % 注释样式
    stringstyle=\ttfamily\color{violet},   % 字符串样式
    columns=fullflexible,                  % 列宽为自适应
    xleftmargin=1em,                       % 左空白1em
    tabsize=4,                             % tab等效空格数
    breaklines=true,                       % 自动断行
    breakatwhitespace=true,                % 只在空白位置断行
    showspaces=false,                      % 显式空格
    showstringspaces=false,              % 不显示字符串中的空格
}
\lstdefinestyle{texstyle}{
    language=Tex,
    numbers=left,
    frame=single,
    numbersep=5pt,              % Margin between line numbers and text
    xleftmargin=17pt,
    framexleftmargin=17pt,
    framexrightmargin=5pt,
    framexbottommargin=4pt,
    basicstyle=\ttfamily, % 设置字体族
    breaklines=true, % 自动换行
    keywordstyle=\bfseries\color{NavyBlue}, % 设置关键字为粗体，颜色为 NavyBlue
    numberstyle=\small\color{verylightgray} ,
}
\lstdefinestyle{pythonstyle}{
    language=Python,                       % 语言设置为 Python
    backgroundcolor=\color[HTML]{FFFBF0},  % 背景颜色为浅灰色
    breaklines=true,                       % 自动将长的代码行换行排版
    numbers=left,                          % 行号显示在左侧
    frame=single,                          % 代码框为单线框
    rulecolor=\color{gray},                % 代码框颜色为灰色
    numberstyle=\color{gray},              % 行号颜色为灰色
    framesep=3em,                          % 同时控制上下和左右边框与代码的距离为 3em
    basicstyle=\ttfamily\small,            % 设置代码字体为等宽字体，小号
    keywordstyle=\bfseries\color{NavyBlue},% 设置关键字为粗体，颜色为蓝色
    commentstyle=\color{DarkGreen},            % 注释样式，颜色为绿色
    stringstyle=\ttfamily\color{purple},   % 字符串样式，等宽字体，颜色为紫色
    columns=fullflexible,                  % 列宽为自适应
    stepnumber=1,                          % 行号递增为 1
    xleftmargin=1em,                       % 代码框与页面的左边距为 1em
    tabsize=4,                             % tab 等效为空格数为 4
    breakatwhitespace=true,                % 只在空白位置断行
    showspaces=false,                      % 不显示空格
    showstringspaces=false,                 % 不显示字符串中的空格
    aboveskip=0.5em,                         % 代码块与上方文字段落的垂直间距
    belowskip=0.5em,                          % 代码块与下方文字段落的垂直间距
}

% 使用
% \begin{lstlisting}[style=pythonstyle]
% def fun():
% print('你好，世界') #我是注释
% \end{lstlisting}

% 代码中插入公式
% \begin{lstlisting}[style=demostyle,mathescape=true]
%     /* 
%      * 定义点
%      *  ------
%      *  | 内部点
%      *  | $x_1= a cos(2\pi \frac{i}{n})$  
%      *  | $y_1= a sin(2\pi \frac{i}{n})$
%      *  ------
% \end{lstlisting}
% \begin{lstlisting}[style=Cstyle,mathescape=true]
%     /* 
%      *  | 内部点
%      *  | $\textcolor{DarkGreen}{x_1= a cos(2\pi \frac{i}{n})}$  
%      *  | $\textcolor{DarkGreen}{y_1= a sin(2\pi \frac{i}{n})}$
% \end{lstlisting}

\lstdefinelanguage{Solidity}{
	keywords=[1]{anonymous, assembly, assert, balance, break, call, callcode, case, catch, class, constant, continue, constructor, contract, debugger, default, delegatecall, delete, do, else, emit, event, experimental, export, external, false, finally, for, function, gas, if, implements, import, in, indexed, instanceof, interface, internal, is, length, library, log0, log1, log2, log3, log4, memory, modifier, new, payable, pragma, private, protected, public, pure, push, require, return, returns, revert, selfdestruct, send, solidity, storage, struct, suicide, super, switch, then, this, throw, transfer, true, try, typeof, using, value, view, while, with, addmod, ecrecover, keccak256, mulmod, ripemd160, sha256, sha3}, % generic keywords including crypto operations
	keywordstyle=[1]\color{blue}\bfseries,
	keywords=[2]{address, bool, byte, bytes, bytes1, bytes2, bytes3, bytes4, bytes5, bytes6, bytes7, bytes8, bytes9, bytes10, bytes11, bytes12, bytes13, bytes14, bytes15, bytes16, bytes17, bytes18, bytes19, bytes20, bytes21, bytes22, bytes23, bytes24, bytes25, bytes26, bytes27, bytes28, bytes29, bytes30, bytes31, bytes32, enum, int, int8, int16, int24, int32, int40, int48, int56, int64, int72, int80, int88, int96, int104, int112, int120, int128, int136, int144, int152, int160, int168, int176, int184, int192, int200, int208, int216, int224, int232, int240, int248, int256, mapping, string, uint, uint8, uint16, uint24, uint32, uint40, uint48, uint56, uint64, uint72, uint80, uint88, uint96, uint104, uint112, uint120, uint128, uint136, uint144, uint152, uint160, uint168, uint176, uint184, uint192, uint200, uint208, uint216, uint224, uint232, uint240, uint248, uint256, var, void, ether, finney, szabo, wei, days, hours, minutes, seconds, weeks, years},	% types; money and time units
	keywordstyle=[2]\color{teal}\bfseries,
	keywords=[3]{block, blockhash, coinbase, difficulty, gaslimit, number, timestamp, msg, data, gas, sender, sig, value, now, tx, gasprice, origin},	% environment variables
	keywordstyle=[3]\color{violet}\bfseries,
	identifierstyle=\color{black},
	sensitive=true,
	comment=[l]{//},
	morecomment=[s]{/*}{*/},
	commentstyle=\color{gray}\ttfamily,
	stringstyle=\color{red}\ttfamily,
	morestring=[b]',
	morestring=[b]"
}
\lstdefinestyle{Soliditystyle}{
    language=Solidity,
    backgroundcolor=\color{Beige},
	extendedchars=true,
	basicstyle=\footnotesize\ttfamily,
	showstringspaces=false,
	showspaces=false,
	numbers=left,
	numberstyle=\footnotesize,
	numbersep=9pt,
	tabsize=2,
	breaklines=true,
	showtabs=false,
	captionpos=b
}


% 页边图标 Column Table
% \columntable[页边距离]{#2表格高度}{#3表格内容}{#4表格标题}
\newcommand{\columntable}[5][0pt]{ % 5个参数，第一个参数是可选参数，表示页边距离
    \ifebook % 如果是电子书
        \par % 首先插入一个段落换行\par
        \captionsetup{type=table} % 设置标题的类型为表格\captionsetup{type=table}
        % 开始一个居中的表格环境
        % 一个两列的表格，每列宽度都是2英寸
        \begin{center}\begin{tabular}{p{2in}p{2in}}
        \fcolorbox{TableBorder}{TableBackground}{ % 创建一个带有边框和背景颜色的盒子
        \vspace{2pt} % 在盒子顶部添加了2点的垂直空间
        \begin{minipage}[t][#2]{1.8in} % 创建一个高度为#2的minipage，宽度为1.8英寸
        \footnotesize \RaggedRight
        #3
        \end{minipage}
        }
        &
        \captionof{table}{#4}
        \end{tabular}\end{center}
    \else
    \marginpar{\captionsetup{type=table} \vspace{#1}
    \fcolorbox{TableBorder}{TableBackground}{
    \begin{minipage}[t][#2]{1.8in}
    \smallskip % 在盒子顶部添加了2点的垂直空间
    \footnotesize \RaggedRight
    #3 % 表格内容
    \end{minipage}
    } \captionof{table}{#4} }
    \fi
    }

% \definecolor{LightBlue}{rgb}{.8,.9,1}

% 定义 介绍人物 的命令
\newcommand{\personfeature}[5][0pt]{
    \ifebook
        \begin{figure}[b]
        \begin{center}\fcolorbox{TableBorder}{TableBackground}{\begin{tabular}{p{2in}p{2.5in}}
        \raisebox{-\height+0.45\baselineskip}{\includegraphics[width=2in]{#2}}
          &
        \scriptsize \RaggedRight
        \textbf{#3} (#4) #5
          \\
        \end{tabular}}\end{center}
        \end{figure}
    \else\marginpar{\vskip#1\sf
    \scriptsize \RaggedRight \centerline{\includegraphics{#2}}\par\vspace{0.1in}
    \textbf{#3} (#4) #5}\fi}

% define the bars to set off derivation sections
 \setlength{\changebarsep}{-3pt}
 \setlength{\changebarwidth}{2pt}
 \definecolor{BarColor}{rgb}{.1,.3,.6}
% \definecolor{DeriveColor}{rgb}{.8,.3,.6}
 \definecolor{DeriveColor}{rgb}{.85,.2,.25}
 \definecolor{NoteColor}{rgb}{0.1,.6,.12}
 \cbcolor{BarColor}

\definecolor{TableBackground}{cmyk}{0.1,0,0,0}
\definecolor{TableBorder}{cmyk}{1,0.2,0,0}

% 定义 举例 环境
\newcounter{example}[chapter]
\renewcommand{\theexample}{\thechapter.\arabic{example}}
\RequirePackage{ifpdf}
\ifpdf
    \renewcommand{\theHexample}{\thechapter.\arabic{example}} %This is needed to keep unique links for hyperref
\fi


\renewcommand{\thefigure}{\thechapter.\arabic{figure}}
\RequirePackage{ifpdf}
\ifpdf
    \renewcommand{\theHfigure}{\thechapter.\arabic{figure}} %This is needed to keep unique links for hyperref
\fi

%\newenvironment{example}[1]
%    {\cbcolor{BarColor}\par \vspace{8pt} \cbstart
%    \begin{enumerate}\item[]
%     \refstepcounter{example}\noindent\textbf{Example \theexample}
%     \par\vspace{5pt}\small\noindent\noindent#1
%     \par\vspace{20pt}\noindent\textbf{Solution:}
%    }
%    {\end{enumerate} \cbend\par \vspace{10pt}}
%\RequirePackage{enumerate} 模板里已经有了 `enumitem` 包，不能加载 `enumerate` 包，这两个包是冲突的。
\RequirePackage{enumitem} % enumerate 自定义编号
\newenvironment{example}
    {\cbcolor{BarColor}\par \vspace{10pt} \begin{changebar}
    \begin{enumerate}\item[]
     \refstepcounter{example}\noindent\textbf{例子
     \theexample} } {\end{enumerate} \end{changebar}\par \vspace{8pt}}

\newcommand{\exProblem}{\par\vspace{2pt}\small\noindent\noindent}
\newcommand{\exSolution}{\par\vspace{10pt}\noindent\textbf{方法:} }

\newenvironment{derivation}[1]
    {\cbcolor{DeriveColor}\par \vspace{10pt}
     \begin{changebar}
    \begin{enumerate}\item[]
     \noindent\textbf{#1}
     \par\vspace{5pt}\small\noindent
   } {\end{enumerate}
 \end{changebar}\par \vspace{10pt}}


\newcommand{\ExSection}[1][ ]{
    \clearpage
    \section*{Exercises}
    \markright{Exercises}
    \addcontentsline{toc}{section}{Exercises}
    \WriteChap{Chapter \thechapter\ Solutions}
}

% \hfill命令告诉LaTeX尽可能多地填充空间以使得后面内容位于页面的右侧
\newenvironment{exercises}[1]
    {\noindent \subsubsection[Exercises]{\emph{Exercises for \ref{#1} \nameref{#1} }}
     \begin{list}{\textbf{P\arabic{problem}\hfill}}{
        \setlength{\listparindent}{0in}
        \setlength{\labelwidth}{0.5in}
        \setlength{\itemindent}{0in}
        \setlength{\leftmargin}{0.65in}}
    }
    {\end{list}}

\newenvironment{review}[1]
    {\noindent \subsubsection*{#1}
     \begin{list}{\textbf{R\arabic{revproblem}\hfill}}{
        \setlength{\listparindent}{0in}
        \setlength{\labelwidth}{0.5in}
        \setlength{\itemindent}{0in}
        \setlength{\leftmargin}{0.65in}}
    }
    {\end{list}}

\newwrite\solutions
\immediate\openout\solutions=\jobname.sln
\newcommand{\WritePLine}[2]{
    \immediate\write\solutions{\string\section*{#1 {\string\footnotesize \string\hyperref[#2]{(#2)} \string\normalsize}}}
    \immediate\write\solutions{ \string\addcontentsline{toc}{section}{#1 (#2)}}
    \immediate\write\solutions{ \string\markboth{\leftmark}{Solutions: #1}}
    \immediate\write\solutions{ \string\begin{itemize}}
    \immediate\write\solutions{ \string\item[]}
    \immediate\write\solutions{ \string\InputIfFileExists{solutions/#2}{}{No Solution File Found}}
    \immediate\write\solutions{ \string\end{itemize} \string\hrule}
    }

 \newcommand{\WriteChap}[1]{
    \immediate\write\solutions{\string\chapter*{#1}}
    \immediate\write\solutions{\string\addcontentsline{toc}{chapter}{#1}}
    }

\RequirePackage{tocloft}
\newcommand{\listproblemname}{}
\newlistof[chapter]{problem}{prb}{\listproblemname}

\newcommand{\prob}[1][prob:P\theproblem]
    {\phantomsection \refstepcounter{problem}\WritePLine{P\theproblem}{#1}
     \item[\textbf{P\theproblem}\hfill]\label{#1}}

\newcounter{subproblem}[problem]
\renewcommand{\thesubproblem}{\theproblem(\alph{subproblem})}
\renewcommand{\theHsubproblem}{\theproblem(\alph{subproblem})} %This is needed to keep unique links for hyperref
\newcommand{\subprob}{\refstepcounter{subproblem}\item[(\alph{subproblem})]}


\newcommand{\lab}[1][lab:L\theproblem]
    {\refstepcounter{problem}\WritePLine{L\theproblem}{#1}
     \item[\textbf{L\theproblem}\hfill]\label{#1}}

\newcounter{revprob}

\newcommand{\rev}[1][rev:R\theproblem]
    {\refstepcounter{revprob}\WritePLine{R\therevprob}{#1}
     \item[\textbf{R\therevprob}\hfill]\label{#1}}

\newenvironment{solution}
    {\par \rule{4.35in}{0.25pt} \nopagebreak \par
    \nopagebreak \scriptsize Solution: \nopagebreak   }
    {\par \nopagebreak \rule{4.35in}{0.25pt} \par \normalsize}

\newenvironment{answer}
    {\par \scriptsize Answer:}
    {\par \normalsize}



\newcommand{\outnote}[2][0pt]{\marginnote{\color{NoteColor}{#2}}[#1]}
\newcommand{\innote}[1]{\textrm{\color{NoteColor}{#1}}}

% Needs mathtools package
\newtagform{numnoteformat}{(}{)}
\newcommand{\numnote}[1]{\renewtagform{numnoteformat}{{\color{NoteColor}{#1}}~~(}{)}\usetagform{numnoteformat}}

\ifebook
    \setlength{\marginparwidth}{0in}
    \setlength{\marginparsep}{0in}
    \setlength{\oddsidemargin}{-0.75in}
    \setlength{\textwidth}{5in}
    \setlength{\topmargin}{-0.75in}
    \setlength{\headheight}{0.3in}
    \setlength{\headsep}{0.1in}
    \setlength{\textheight}{500cm}
    \setlength{\footskip}{0in}
    \fancyheadoffset[LE,RO]{\marginparsep+\marginparwidth}

    \RequirePackage{everyshi}
    \pagestyle{empty}
    \textheight500cm
    \pdfpageheight500cm
    \makeatletter
    \EveryShipout{\pdfpageheight=\pagetotal
    \advance\pdfpageheight by 2in
    \advance\pdfpageheight by \topmargin
    \advance\pdfpageheight by \footskip
    \advance\pdfpageheight by \textheight
    \advance\pdfpageheight by -\pagegoal}
    \makeatother

    % Each section is its own "page"
    \let\stdsection\section
    \renewcommand\section{\pagebreak\stdsection}

    % the index can't be two column, so disallow this environment
    \renewcommand{\twocolumn}[1][]{#1}

    % Get rid of margin content
    \renewcommand{\outnote}[1]{\numnote{#1}}
    \AtBeginDocument{\pdfpageheight=500cm \pdfpagewidth=5.5in}
    \pagestyle{empty}
    \renewcommand{\sectionmark}[1]{\markright{\leftmark}}
\else

\fi



