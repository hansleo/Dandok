-- --------------------------------------------------------
-- 호스트:                          127.0.0.1
-- 서버 버전:                        10.1.14-MariaDB - mariadb.org binary distribution
-- 서버 OS:                        Win64
-- HeidiSQL 버전:                  9.1.0.4867
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- 테이블 dandock의 구조를 덤프합니다. target_site
DROP TABLE IF EXISTS `target_site`;
CREATE TABLE IF NOT EXISTS `target_site` (
  `part` int(11) DEFAULT NULL,
  `url` varchar(400) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Dumping data for table dandock.target_site: ~9 rows (대략적)
/*!40000 ALTER TABLE `target_site` DISABLE KEYS */;
INSERT INTO `target_site` (`part`, `url`) VALUES
	(2, 'http://news.naver.com/main/search/search.nhn?refresh=&so=datetime.dsc&stPhoto=&stPaper=&stRelease=&ie=MS949&detail=0&rcsection=exist%3A101&query=%B4%DC%B5%B6&x=16&y=14&sm=title.basic&pd=4&startDate=stDt&endDate=enDt=&page=1'),
	(3, 'http://news.naver.com/main/search/search.nhn?refresh=&so=datetime.dsc&stPhoto=&stPaper=&stRelease=&ie=MS949&detail=0&rcsection=exist%3A102&query=%B4%DC%B5%B6&x=16&y=14&sm=title.basic&pd=4&startDate=stDt&endDate=enDt=&page=1'),
	(7, 'http://news.naver.com/main/search/search.nhn?refresh=&so=datetime.dsc&stPhoto=&stPaper=&stRelease=&ie=MS949&detail=0&rcsection=exist%3A103&query=%B4%DC%B5%B6&x=16&y=14&sm=title.basic&pd=4&startDate=stDt&endDate=enDt=&page=1'),
	(9, 'http://news.naver.com/main/search/search.nhn?refresh=&so=datetime.dsc&stPhoto=&stPaper=&stRelease=&ie=MS949&detail=0&rcsection=exist%3A104&query=%B4%DC%B5%B6&x=16&y=14&sm=title.basic&pd=4&startDate=stDt&endDate=enDt=&page=1'),
	(6, 'http://news.naver.com/main/search/search.nhn?refresh=&so=datetime.dsc&stPhoto=&stPaper=&stRelease=&ie=MS949&detail=0&rcsection=exist%3A105&query=%B4%DC%B5%B6&x=16&y=14&sm=title.basic&pd=4&startDate=stDt&endDate=enDt=&page=1'),
	(4, 'http://news.naver.com/main/search/search.nhn?refresh=&so=datetime.dsc&stPhoto=&stPaper=&stRelease=&ie=MS949&detail=0&rcsection=exist%3A106&query=%B4%DC%B5%B6&x=16&y=14&sm=title.basic&pd=4&startDate=stDt&endDate=enDt=&page=1'),
	(8, 'http://news.naver.com/main/search/search.nhn?refresh=&so=datetime.dsc&stPhoto=&stPaper=&stRelease=&ie=MS949&detail=0&rcsection=exist%3A110&query=%B4%DC%B5%B6&x=16&y=14&sm=title.basic&pd=4&startDate=stDt&endDate=enDt=&page=1'),
	(5, 'http://news.naver.com/main/search/search.nhn?refresh=&so=datetime.dsc&stPhoto=&stPaper=&stRelease=&ie=MS949&detail=0&rcsection=exist%3A107&query=%B4%DC%B5%B6&x=16&y=14&sm=title.basic&pd=4&startDate=stDt&endDate=enDt=&page=1'),
	(1, 'http://news.naver.com/main/search/search.nhn?refresh=&so=datetime.dsc&stPhoto=&stPaper=&stRelease=&ie=MS949&detail=0&rcsection=exist%3A100&query=%B4%DC%B5%B6&x=16&y=14&sm=title.basic&pd=4&startDate=stDt&endDate=enDt=&page=1');
/*!40000 ALTER TABLE `target_site` ENABLE KEYS */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
