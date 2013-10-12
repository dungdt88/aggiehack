<?php

namespace Visa\RouteFinderBundle\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\Controller;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Visa\RouteFinderBundle\Service\RouteFinder;

/**
 * Class DefaultController
 * @package Visa\RouteFinderBundle\Controller
 */
class DefaultController extends Controller
{
    /**
     * @return \Symfony\Component\HttpFoundation\Response
     */
    public function indexAction()
    {
        return $this->render('VisaRouteFinderBundle:Default:index.html.twig');
    }

    /**
     * @return Response
     */
    public function ajaxCalculateRouteAction()
    {
        /** @var $request Request */
        $request = $this->getRequest();

        $data = $request->request->all();
        $responseData = array();
        $responseData['error'] = true;

        if (empty($data['from_coordinate_lat']) || empty($data['from_coordinate_lat'])
            || empty($data['from_coordinate_lat']) || empty($data['from_coordinate_lat'])
            || empty($data['from_coordinate_lat'])) {
            return new JsonResponse($responseData);
        }
        
        /** @var $routeFinder RouteFinder */
        $routeFinder = $this->get('visa_route_finder.service.route_finder');
        
        $routes = $routeFinder->findRoutes(
            $data['from_coordinate_lat'],
            $data['from_coordinate_long'],
            $data['to_coordinate_lat'],
            $data['to_coordinate_long'],
            $data['start_time']
        );
        $responseData['error'] = false;
        
        $responseData['routes'] = $routes;
        
        return new JsonResponse($responseData);
    }
}
