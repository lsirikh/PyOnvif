# Python ONVIF Control

Python에서 ONVIF 카메라의 PTZ와 포커스 기능을 호출하는 라이브러리입니다. `onvif-zeep`과 WSDL을 사용하며, 카메라 연결 설정과 기능별 요청을 분리합니다.

## 구성

- [Onvif](Onvif): 서비스 초기화, PTZ, 포커스, 요청 처리
- [Config](Config): 설정 데이터 처리
- [wsdl](wsdl): ONVIF 서비스 정의
- [test.py](test.py): 장비 연결 예제

## 실행 준비

기존 개발 환경은 Python 3.9입니다. [requirements.txt](requirements.txt)의 의존성을 설치한 후 카메라 주소·ONVIF 포트·계정 설정을 맞춰 사용합니다. `test.py`는 장비에 명령을 보낼 수 있는 예제이므로, 실행 전 호출 내용을 확인해야 합니다.

기존 개발 표기: Sensorway Co., Ltd., GH, 2022-11-18. 카메라별 ONVIF 지원 범위에 따라 동작이 달라질 수 있습니다.
