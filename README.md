# Parsed PDF objects to Tree structure Converter

[pdf-parser.py](https://blog.didierstevens.com/programs/pdf-tools/)로 파싱된 문자열을 파싱하여 트리 구조로 변환한다.

## 0. 환경

python 3.7 기준으로 작성되었다.

## 1. 개요

다음과 같이 pdf-parser.py로 파싱된 문자열을 파싱 및 구조화 하여 트리 구조로 변환한다.

<img src="./img1.png" alt="" width="500"/>

## 2. 트리 구조

트리 구조는 `Vertex`인스턴스로 이루어진 리스트 `G`로 저장된다.

각 정점은 `Vertex`인스턴스로 나타내어 지며, `G`에서의 인덱스를 고유값으로 가진다.

자식에 접근할 때 `G`에서의 인덱스를 이용하여 접근한다.

### 2.1. Vertex 클래스

`Vertex`는 다음과 같은 변수를 가진다.
* type: 해당 정점의 타입을 나타내는 정수 (1 ~ 4의 값을 가진다)
* child: 해당 정점의 자식 정점의 인덱스 정보를 담는다.
  * type에 따라 사전 타입(edge의 이름이 있는 경우), 리스트(edge의 이름이 없는 경우), None(자식이 없는 경우)으로 결정된다.
* name: 해당 정점의 이름(값)을 나타내는 문자열

### 2.2. Vertex의 종류 (type)

각 `Vertex`는 다음 중 하나의 타입을 가진다.
* **obj (type = 1)**: child를 사전으로 가지고 있다. - 오브젝트
* **item (type = 2)**: child를 가지고 있지 않다. - 문자열
* **dict (type = 3)**: child를 사전으로 가지고 있다. - <<, >> 로 둘러싸인 사전 타입 원소
* **arr (type = 4)**: child를 리스트로 가지고 있다. - \[, ] 로 둘러싸인 배열 타입 원소

child가 사전일 경우, key값이 해당 edge의 이름을 나타낸다.
